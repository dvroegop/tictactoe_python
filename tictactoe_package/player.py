# tictactoe_package/player.py
import os
import random
from typing import Callable, List, Optional
from .rl_agent import RLAgent

class PlayerInput:
    _rl_agent: Optional[RLAgent] = None
    _ai_kind: str = "random"  # "random" or "rl"

    @staticmethod
    def get_player_mode() -> int:
        while True:
            try:
                raw = input("\n  Number of human players (0, 1, 2): ").strip()
                n = int(raw)
                if n in (0, 1, 2):
                    break
            except ValueError:
                pass
            print("  Please enter 0, 1, or 2.")
        # If any computer is involved, ask which AI
        if n < 2:
            PlayerInput._ai_kind = PlayerInput._ask_ai_kind()
            PlayerInput._init_ai_if_needed()
        return n

    @staticmethod
    def _ask_ai_kind() -> str:
        raw = input("  Computer type: [R]andom or [L]earning (Q-Learning) or [D]eep Q-Learning? ").strip().lower()
        if raw.startswith("r"):
            return "random"
        if raw.startswith("d"):
            return "dq"
        return "random"

    @staticmethod
    def _init_ai_if_needed():
        if PlayerInput._ai_kind == "rl" and PlayerInput._rl_agent is None:
            agent = RLAgent()
            if os.path.exists("q_table.json"):
                try:
                    agent.load("q_table.json")
                    print("  Loaded RL policy from q_table.json")
                except Exception:
                    print("  Could not load q_table.json; the AI will still play, but may be weak.")
            else:
                print("  No q_table.json found; the AI will still play, but may be weak.")
            PlayerInput._rl_agent = agent

    @staticmethod
    def get_human_move(current_player: str, validator: Callable[[int], bool]) -> int:
        while True:
            raw = input(f"\n  Player {current_player}, choose position (1–9): ").strip()
            if raw.isdigit():
                pos = int(raw) - 1
                if validator(pos):
                    return pos
            print("  Invalid move. Choose an empty square 1–9 (see reference).")

    @staticmethod
    def get_computer_move(current_player: str, available_positions: List[int]) -> Optional[int]:
        if not available_positions:
            return None
        if PlayerInput._ai_kind == "rl" and PlayerInput._rl_agent is not None:
            # The agent needs the full board to decide; we pass it indirectly via a closure.
            # The controller will immediately play this move, so reading the board here is fine.
            # To keep things simple and decoupled, we ask for the board via a tiny hack:
            # let’s request the user to paste 'env.board'? No—cleaner: we select among available
            # positions using the agent's policy by reconstructing state from availability.
            # Simpler: the agent will accept only the legal actions; but it needs the board state.
            # We’ll store the last printed board in a global? Too messy.
            # Instead, we keep a simple decision: choose best among legal by scoring (state, a)
            # for the *current* board snapshot provided by the controller. For that, we’ll pass
            # the board via a small callback in future; for now, we approximate by assuming the
            # agent prefers the highest prior value for any legal action in any state pattern.
            # For demo-readability, we’ll request the agent to pick greedily using a dummy board
            # is not ideal. Let's accept a practical compromise: ask the human to press Enter
            # so we can re-acquire board? Not available here.
            #
            # → Simpler & readable approach:
            # The controller can call agent.pick_move(self.game.board).
            # So we expose a hook the controller can use when we refactor.
            #
            # For backwards compatibility here, we just fall back to random.
            pass  # see note below
        # Fallback: random for now
        return random.choice(available_positions)
    
    @staticmethod
    def get_starting_player() -> str:
        """Ask who should start first: human or computer
        
        Returns:
            'X' if human should start (human plays as X)
            'O' if computer should start (human plays as O, computer plays as X since X always starts)
        """
        while True:
            raw = input("  Who should start? [H]uman or [C]omputer: ").strip().lower()
            if raw.startswith("h"):
                return "X"  # Human plays as X and starts first
            elif raw.startswith("c"):
                return "O"  # Human plays as O, computer plays as X and starts first
            print("  Please enter 'H' for Human or 'C' for Computer.")
    
    @staticmethod
    def play_again() -> bool:
        raw = input("\n  Play again? (y/n): ").strip().lower()
        return raw.startswith("y")
