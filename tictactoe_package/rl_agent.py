# tictactoe_package/rl_agent.py
from __future__ import annotations
from dataclasses import dataclass, field
import json
import random
from typing import Dict, List, Tuple, Optional
from .game import TicTacToe  # uses your clean environment API

State = str     # e.g., "X O  X   "
Action = int    # 0..8 index

def board_to_state(board: List[str], current_player: str) -> State:
    # Turn ['X',' ','O', ...] into a string; simple and readable
    # Append current_player to distinguish between X's turn and O's turn
    return "".join(board) + "|" + current_player

@dataclass
class RLAgent:
    alpha: float = 0.2       # learning rate
    gamma: float = 0.95      # discount
    epsilon: float = 0.10    # exploration during training
    q: Dict[Tuple[State, Action], float] = field(default_factory=dict)

    def value(self, s: State, a: Action) -> float:
        return self.q.get((s, a), 0.0)

    def best_action(self, s: State, legal: List[int]) -> Action:
        # Pick the legal action with highest Q, break ties randomly for clarity
        best = max(legal, key=lambda a: self.value(s, a))
        return best

    def choose_action(self, s: State, legal: List[int], explore: bool) -> Action:
        if explore and random.random() < self.epsilon:
            return random.choice(legal)
        return self.best_action(s, legal)

    def update(self, s: State, a: Action, r: float, s_next: Optional[State], legal_next: List[int]):
        old = self.value(s, a)
        future = 0.0 if s_next is None or not legal_next else max(self.value(s_next, a2) for a2 in legal_next)
        self.q[(s, a)] = old + self.alpha * (r + self.gamma * future - old)

    # ---------- Training by self-play ----------

    def train_self_play(self, episodes: int = 5000, verbose_every: int = 0) -> None:
        """
        Train by having the agent play both X and O.
        Reward shaping:
          +1 for a win, -1 for a loss, 0 for a draw, small -0.01 per move to encourage faster wins.
        """
        for ep in range(1, episodes + 1):
            env = TicTacToe()
            trajectory: List[Tuple[State, Action, str]] = []  # (state, action, playerWhoMoved)

            # Play an episode
            while True:
                mover = env.current_player  # The player who is about to move
                s = board_to_state(env.board, mover)
                legal = env.get_available_positions()
                a = self.choose_action(s, legal, explore=True)
                env.make_move(a)
                trajectory.append((s, a, mover))  # Save state with player who moved

                winner = env.check_winner()
                if winner or env.is_board_full():
                    # Episode ends
                    result_reward = 0.0
                    if winner == 'X':
                        result_reward = +1.0
                    elif winner == 'O':
                        result_reward = +1.0
                    else:
                        result_reward = 0.0  # draw

                    # Assign results from the perspective of each mover:
                    # If the mover's symbol == winner -> +1, else if opponent won -> -1, else 0.
                    # Also add a tiny step penalty to encourage faster endings.
                    for (s_t, a_t, mover) in reversed(trajectory):
                        if winner is None:
                            r = 0.0
                        else:
                            r = +1.0 if mover == winner else -1.0
                        r -= 0.01  # small time penalty
                        self.update(s_t, a_t, r, None, [])
                    break

                # Switch player for next turn
                env.switch_player()

                # Next step update (temporal difference) with step reward ~0 except tiny time penalty
                s_next = board_to_state(env.board, env.current_player)
                legal_next = env.get_available_positions()
                self.update(s, a, -0.01, s_next, legal_next)

        if verbose_every:
            print(f"Training finished for {episodes} episodes. Q-size: {len(self.q)}")

    # ---------- Inference ----------

    def pick_move(self, board: List[str], current_player: str) -> int:
        s = board_to_state(board, current_player)
        legal = [i for i, v in enumerate(board) if v == ' ']
        if not legal:
            return -1
        # During actual play we do NOT explore (deterministic, explainable)
        return self.choose_action(s, legal, explore=False)

    # ---------- Persistence ----------

    def save(self, path: str = "q_table.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({f"{s}|{a}": v for (s, a), v in self.q.items()}, f, indent=2)

    def load(self, path: str = "q_table.json"):
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self.q = {}
        for key, v in raw.items():
            s, a = key.rsplit("|", 1)
            self.q[(s, int(a))] = float(v)
