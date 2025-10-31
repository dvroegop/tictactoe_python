"""
Game controller for TicTacToe
Manages game flow and coordinates between game logic, UI, and players
"""

from .game import TicTacToe
from .ui import GameUI
from .player import PlayerInput


class GameController:
    """Controls the game flow"""
    
    def __init__(self):
        """Initialize game controller"""
        self.game = TicTacToe()
        self.ui = GameUI()
        self.player_input = PlayerInput()
        self.num_human_players = 2
    
    def play_game(self):
        """Main game loop"""
        self.game.reset()
        self.ui.display_positions()
        
        while True:
            self.ui.display_board(self.game.board)
            
            # Determine if current player is human or computer
            if self.game.current_player == 'X':
                is_human = self.num_human_players >= 1
            else:
                is_human = self.num_human_players == 2
            
            # Get and make move
            if is_human:
                position = self.player_input.get_human_move(
                    self.game.current_player,
                    self.game.is_valid_move
                )
                self.game.make_move(position)
            else:
                position = self.player_input.get_computer_move(
                    self.game.current_player,
                    self.game.get_available_positions()
                )
                if position is not None:
                    self.game.make_move(position)
            
            # Check for winner
            winner = self.game.check_winner()
            if winner:
                self.ui.display_board(self.game.board)
                self.ui.display_winner(winner)
                break
            
            # Check for draw
            if self.game.is_board_full():
                self.ui.display_board(self.game.board)
                self.ui.display_draw()
                break
            
            # Switch to next player
            self.game.switch_player()
    
    def run(self):
        """Run the game application"""
        self.ui.clear_screen()
        self.ui.display_title()
        
        while True:
            self.num_human_players = self.player_input.get_player_mode()
            self.ui.clear_screen()
            self.ui.display_title()
            
            if self.num_human_players == 0:
                print("\n  Starting Computer vs Computer game...")
            elif self.num_human_players == 1:
                print("\n  Starting Human vs Computer game...")
                print("  You are Player X")
            else:
                print("\n  Starting Human vs Human game...")
            
            input("\n  Press Enter to start...")
            self.ui.clear_screen()
            
            self.play_game()
            
            if not self.player_input.play_again():
                break
            
            self.ui.clear_screen()
            self.ui.display_title()
        
        self.ui.display_goodbye()
