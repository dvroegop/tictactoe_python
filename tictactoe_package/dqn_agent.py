# dqn_agent.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Deque
from collections import deque
import random
import math
import torch
import torch.nn as nn
import torch.optim as optim

# ----- Utilities -----

def encode_board(board: List[str], current_player: str) -> torch.Tensor:
    """
    One-hot encode each cell: [empty, X, O] => 3 * 9 = 27
    Append current_player scalar (+1 for X, -1 for O) => 28 total inputs.
    """
    mapping = {' ': [1, 0, 0], 'X': [0, 1, 0], 'O': [0, 0, 1]}
    vec = []
    for v in board:
        vec.extend(mapping[v])
    vec.append(1.0 if current_player == 'X' else -1.0)
    return torch.tensor(vec, dtype=torch.float32)

def legal_mask(board: List[str]) -> torch.Tensor:
    """1 for legal actions, 0 for illegal."""
    return torch.tensor([1.0 if v == ' ' else 0.0 for v in board], dtype=torch.float32)

# ----- Network -----

class QNet(nn.Module):
    def __init__(self, in_dim=28, hidden=64, out_dim=9):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)

# ----- Agent -----

@dataclass
class DQNConfig:
    gamma: float = 0.99
    lr: float = 1e-3
    batch_size: int = 64
    buffer_size: int = 50_000
    start_training_after: int = 500       # warm-up transitions
    target_sync_every: int = 500          # steps
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    epsilon_decay_steps: int = 5_000
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    verbose: bool = True                  # print Q-value explanations during action selection

@dataclass
class DQNAgent:
    cfg: DQNConfig = field(default_factory=DQNConfig)
    qnet: QNet = field(init=False)
    target: QNet = field(init=False)
    opt: optim.Optimizer = field(init=False)
    step_count: int = 0
    buffer: Deque = field(default_factory=lambda: deque(maxlen=DQNConfig().buffer_size))

    def __post_init__(self):
        self.qnet = QNet().to(self.cfg.device)
        self.target = QNet().to(self.cfg.device)
        self.target.load_state_dict(self.qnet.state_dict())
        self.opt = optim.Adam(self.qnet.parameters(), lr=self.cfg.lr)
        self.loss_fn = nn.MSELoss()

    # ---------- Policy ----------

    def epsilon(self) -> float:
        # Linear decay
        t = min(self.step_count, self.cfg.epsilon_decay_steps)
        frac = 1 - t / self.cfg.epsilon_decay_steps
        return self.cfg.epsilon_end + (self.cfg.epsilon_start - self.cfg.epsilon_end) * max(0.0, frac)

    @torch.no_grad()
    def select_action(self, board: List[str], current_player: str, explore: bool) -> int:
        mask = legal_mask(board).to(self.cfg.device)   # (9,)
        legal_indices = [i for i, m in enumerate(mask.tolist()) if m > 0.5]
        if not legal_indices:
            return -1

        if explore and random.random() < self.epsilon():
            return random.choice(legal_indices)

        s = encode_board(board, current_player).to(self.cfg.device).unsqueeze(0)  # (1,28)
        q = self.qnet(s).squeeze(0)  # (9,)
        # explain why (only if verbose mode is enabled)
        if self.cfg.verbose:
            vals = q.cpu().numpy().tolist()
            pairs = [(i, vals[i]) for i in range(9) if board[i] == ' ']
            pairs.sort(key=lambda x: x[1], reverse=True)
            print("  [Why] Top candidates:", ", ".join([f"{i+1}: {v:.3f}" for i, v in pairs[:3]]))
        # mask illegal moves by setting them to very low value
        q_masked = q.clone()
        q_masked[mask < 0.5] = -1e9
        return int(torch.argmax(q_masked).item())

    # ---------- Replay memory ----------

    def remember(self, s, a, r, s_next, done):
        self.buffer.append((s, a, r, s_next, done))

    # ---------- Learning ----------

    def can_learn(self) -> bool:
        return len(self.buffer) >= self.cfg.batch_size and self.step_count >= self.cfg.start_training_after

    def learn(self):
        if not self.can_learn():
            return

        batch = random.sample(self.buffer, self.cfg.batch_size)
        s, a, r, s_next, done = zip(*batch)
        s = torch.stack(s).to(self.cfg.device)             # (B, 28)
        a = torch.tensor(a, dtype=torch.long, device=self.cfg.device)  # (B,)
        r = torch.tensor(r, dtype=torch.float32, device=self.cfg.device)  # (B,)
        s_next = torch.stack(s_next).to(self.cfg.device)   # (B, 28)
        done = torch.tensor(done, dtype=torch.float32, device=self.cfg.device)  # (B,)

        # Q(s,a)
        q = self.qnet(s).gather(1, a.view(-1, 1)).squeeze(1)  # (B,)

        # Target: r + gamma * max_a' Q_target(s',a') * (1 - done)
        with torch.no_grad():
            q_next = self.target(s_next).max(1).values
            target = r + self.cfg.gamma * q_next * (1.0 - done)

        loss = self.loss_fn(q, target)
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

        # Periodically sync target network
        if self.step_count % self.cfg.target_sync_every == 0:
            self.target.load_state_dict(self.qnet.state_dict())

    # ---------- Persistence ----------

    def save(self, path="dqn_policy.pt"):
        torch.save(self.qnet.state_dict(), path)

    def load(self, path="dqn_policy.pt"):
        self.qnet.load_state_dict(torch.load(path, map_location=self.cfg.device))
        self.target.load_state_dict(self.qnet.state_dict())

    # ---------- Inference helper for the controller (no exploration) ----------

    @torch.no_grad()
    def pick_move(self, board: List[str], current_player: str) -> int:
        return self.select_action(board, current_player, explore=False)
