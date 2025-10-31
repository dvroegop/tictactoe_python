"""
Player input handling for TicTacToe
Manages human and computer player interactions
"""

import random


class PlayerInput:
    """Handles player input and move selection"""
    
    @staticmethod
    def get_player_mode():
        """Get the number of human players"""
        while True:
            print("\n" + "-"*50)
            print("  Select game mode:")
            print("-"*50)
            print("  [0] Computer vs Computer")
            print("  [1] Human vs Computer")
            print("  [2] Human vs Human")
            print("-"*50)
            
            try:
                choice = input("\n  Enter your choice (0/1/2): ").strip()
                if choice in ['0', '1', '2']:
                    return int(choice)
                else:
                    print("\n  ERROR: Please enter 0, 1, or 2.")
            except (ValueError, KeyboardInterrupt):
                print("\n  ERROR: Invalid input.")
    
    @staticmethod
    def get_human_move(player_symbol, is_valid_move_func):
        """Get move from human player"""
        while True:
            try:
                print(f"\n  Player {player_symbol}'s turn")
                move = input("  Enter position (1-9): ").strip()
                
                if not move.isdigit():
                    print("  ERROR: Please enter a number.")
                    continue
                    
                position = int(move) - 1  # Convert to 0-based index
                
                if position < 0 or position > 8:
                    print("  ERROR: Position must be between 1 and 9.")
                    continue
                    
                if not is_valid_move_func(position):
                    print("  ERROR: That position is already taken.")
                    continue
                    
                return position
                
            except (ValueError, KeyboardInterrupt):
                print("  ERROR: Invalid input.")
    
    @staticmethod
    def get_computer_move(player_symbol, available_positions):
        """Get move from computer (random available position)"""
        if available_positions:
            position = random.choice(available_positions)
            print(f"\n  Computer ({player_symbol}) is thinking...")
            print(f"  Computer selects position {position + 1}")
            input("  Press Enter to continue...")
            return position
        return None
    
    @staticmethod
    def play_again():
        """Ask if players want to play again"""
        while True:
            print()
            choice = input("  Play again? (Y/N): ").strip().upper()
            if choice in ['Y', 'YES']:
                return True
            elif choice in ['N', 'NO']:
                return False
            else:
                print("  ERROR: Please enter Y or N.")
