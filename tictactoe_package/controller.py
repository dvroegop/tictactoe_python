"""
Game controller for TicTacToe
Manages game flow and coordinates between game logic, UI, and players
"""

from typing import Optional
from .game import TicTacToe
from .ui import GameUI
from .player import PlayerInput
from .rl_agent import RLAgent
from .dqn_agent import DQNAgent
import random


class GameController:
    """Controls the game flow"""
    
    def __init__(self):
        """Initialize game controller"""
        self.game = TicTacToe()
        self.num_human_players = 2
        self._rl_agent: Optional[RLAgent] = None
        self._dq_agent: Optional[DQNAgent] = None
    
    def play_game(self):
        """Main game loop"""
        self.game.reset()
        GameUI.display_positions()
        
        while True:
            GameUI.display_board(self.game.board)
            
            # Determine if current player is human or computer
            if self.game.current_player == 'X':
                is_human = self.num_human_players >= 1
            else:
                is_human = self.num_human_players == 2
            
            # Get and make move
            if is_human:
                position = PlayerInput.get_human_move(
                    self.game.current_player,
                    self.game.is_valid_move
                )
                self.game.make_move(position)
            else:
                # computer move
                if PlayerInput._ai_kind == "rl":
                    # Init once if chosen
                    if self._rl_agent is None:
                        self._rl_agent = RLAgent()
                        try:
                            self._rl_agent.load("q_table.json")
                            print("  [AI] RL policy loaded.")
                        except Exception:
                            print("  [AI] No policy loaded; using random fallback.")
                    # Let RL pick based on the actual board
                    if self._rl_agent:
                        position = self._rl_agent.pick_move(self.game.board)
                        if position not in self.game.get_available_positions():
                            # Safety: fallback
                            position = PlayerInput.get_computer_move(
                                self.game.current_player,
                                self.game.get_available_positions()
                            )
                    else:
                        position = PlayerInput.get_computer_move(
                            self.game.current_player,
                            self.game.get_available_positions()
                        )
                elif PlayerInput._ai_kind == "dq":
                    # Use DQN agent to pick move
                    if self._dq_agent is None:
                        self._dq_agent = DQNAgent()
                        try:
                            self._dq_agent.load("dqn_policy.pt")
                            print("  [AI] DQN policy loaded.")
                        except Exception:
                            print("  [AI] No DQN policy loaded; using random fallback.")
                            PlayerInput._ai_kind = "random"  # fallback
                            self._dq_agent = None
                    if self._dq_agent is not None:
                        position = self._dq_agent.pick_move(self.game.board, self.game.current_player)
                        if position not in self.game.get_available_positions():
                            position = random.choice(self.game.get_available_positions())
                    else:
                        position = random.choice(self.game.get_available_positions())
                else:
                    position = PlayerInput.get_computer_move(
                        self.game.current_player,
                        self.game.get_available_positions()
                    )
                if position is not None:
                    self.game.make_move(position)
                    
            # Check for winner
            winner = self.game.check_winner()
            if winner:
                GameUI.display_board(self.game.board)
                GameUI.display_winner(winner)
                break
            
            # Check for draw
            if self.game.is_board_full():
                GameUI.display_board(self.game.board)
                GameUI.display_draw()
                break
            
            # Switch to next player
            self.game.switch_player()
    
    def run(self):
        """Run the game application"""
        GameUI.clear_screen()
        GameUI.display_title()
        
        while True:
            self.num_human_players = PlayerInput.get_player_mode()
            GameUI.clear_screen()
            GameUI.display_title()
            
            if self.num_human_players == 0:
                print("\n  Starting Computer vs Computer game...")
            elif self.num_human_players == 1:
                print("\n  Starting Human vs Computer game...")
                print("  You are Player X")
            else:
                print("\n  Starting Human vs Human game...")
            
            input("\n  Press Enter to start...")
            GameUI.clear_screen()
            
            self.play_game()
            
            if not PlayerInput.play_again():
                break
            
            GameUI.clear_screen()
            GameUI.display_title()
        
        GameUI.display_goodbye()
