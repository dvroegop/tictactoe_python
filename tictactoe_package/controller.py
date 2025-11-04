"""
Game controller for TicTacToe
Manages game flow and coordinates between game logic, UI, and players
"""

from typing import Optional
from .game import TicTacToe
from .ui import GameUI
from .player import PlayerInput
from .rl_agent import RLAgent
try:
    from .dqn_agent import DQNAgent
except ImportError:
    DQNAgent = None
import random


class GameController:
    """Controls the game flow"""
    
    def __init__(self):
        """Initialize game controller"""
        self.game = TicTacToe()
        self.num_human_players = 2
        self.human_player_symbol = 'X'  # Track which symbol the human player uses
        self._rl_agent: Optional[RLAgent] = None
        # Note: Can't use Optional[DQNAgent] since DQNAgent may be None (module not available)
        self._dq_agent = None  # DQNAgent instance or None
    
    def _get_ai_move(self):
        """Get computer move based on current AI type
        
        Returns:
            int or None: Position to move (0-8) or None if no valid move
        """
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
                position = self._rl_agent.pick_move(self.game.board, self.game.current_player)
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
                if DQNAgent is None:
                    print("  [AI] DQN not available (torch not installed); using random fallback.")
                    PlayerInput._ai_kind = "random"
                else:
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
        return position
    
    def play_game(self):
        """Main game loop"""
        self.game.reset()
        GameUI.display_positions()
        
        # Prepare the board area once at the start
        GameUI.prepare_board_area()
        
        while True:
            GameUI.display_board(self.game.board)
            
            # Determine if current player is human or computer
            if self.num_human_players == 2:
                # Both players are human
                is_human = True
            elif self.num_human_players == 1:
                # One human player - check if current player matches human symbol
                is_human = (self.game.current_player == self.human_player_symbol)
            else:
                # No human players
                is_human = False
            
            # Get and make move
            if is_human:
                position = PlayerInput.get_human_move(
                    self.game.current_player,
                    self.game.is_valid_move
                )
                self.game.make_move(position)
            else:
                # computer move
                position = self._get_ai_move()
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
                # Ask who should start first
                self.human_player_symbol = PlayerInput.get_starting_player()
                if self.human_player_symbol == 'X':
                    print("\n  Starting Human vs Computer game...")
                    print("  You are Player X and will start first")
                else:
                    print("\n  Starting Human vs Computer game...")
                    print("  You are Player O and the computer will start first")
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
    
    def play_game_auto(self):
        """Play a single game in auto mode (computer vs computer, no UI)
        
        Returns:
            str or None: Winner ('X', 'O') or None for draw
        """
        self.game.reset()
        
        while True:
            # Get computer move using shared helper
            position = self._get_ai_move()
            
            if position is not None:
                self.game.make_move(position)
            
            # Check for winner
            winner = self.game.check_winner()
            if winner:
                return winner
            
            # Check for draw
            if self.game.is_board_full():
                return None  # Draw
            
            # Switch to next player
            self.game.switch_player()
    
    def run_auto(self, num_games):
        """Run multiple games in auto mode (computer vs computer)
        
        Args:
            num_games: Number of games to play
        """
        print("\n==================================================")
        print("           TIC TAC TOE - AUTO MODE")
        print("==================================================")
        print(f"\n  Running {num_games} games (Computer vs Computer)...")
        print("  Please wait...\n")
        
        # Set to computer vs computer mode
        self.num_human_players = 0
        
        # Ask which AI type to use
        PlayerInput._ai_kind = PlayerInput._ask_ai_kind()
        
        # Statistics
        wins_x = 0
        wins_o = 0
        draws = 0
        
        # Play all games
        for i in range(num_games):
            winner = self.play_game_auto()
            if winner == 'X':
                wins_x += 1
            elif winner == 'O':
                wins_o += 1
            else:
                draws += 1
            
            # Show progress every 10 games
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1} / {num_games} games...")
        
        # Display results
        print("\n==================================================")
        print("                   RESULTS")
        print("==================================================")
        print(f"\n  Total games played: {num_games}")
        print(f"\n  Player X wins:      {wins_x:4d}  ({wins_x / num_games * 100:5.1f}%)")
        print(f"  Player O wins:      {wins_o:4d}  ({wins_o / num_games * 100:5.1f}%)")
        print(f"  Draws:              {draws:4d}  ({draws / num_games * 100:5.1f}%)")
        print("\n==================================================\n")
