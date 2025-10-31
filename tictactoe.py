#!/usr/bin/env python3
"""
TicTacToe Game - Console Edition
Inspired by 80's style computer games
"""

import random
import os


class TicTacToe:
    """Main TicTacToe game class"""
    
    def __init__(self):
        """Initialize the game board"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        
    def display_board(self):
        """Display the game board with 80's style formatting"""
        print("\n" + "="*50)
        print("                  TIC TAC TOE")
        print("="*50)
        print()
        print("     |     |     ")
        print(f"  {self.board[0]}  |  {self.board[1]}  |  {self.board[2]}  ")
        print("     |     |     ")
        print("-----+-----+-----")
        print("     |     |     ")
        print(f"  {self.board[3]}  |  {self.board[4]}  |  {self.board[5]}  ")
        print("     |     |     ")
        print("-----+-----+-----")
        print("     |     |     ")
        print(f"  {self.board[6]}  |  {self.board[7]}  |  {self.board[8]}  ")
        print("     |     |     ")
        print()
        print("="*50)
        
    def display_positions(self):
        """Display position numbers for reference"""
        print("\n" + "-"*50)
        print("         Position Reference:")
        print("-"*50)
        print()
        print("     |     |     ")
        print("  1  |  2  |  3  ")
        print("     |     |     ")
        print("-----+-----+-----")
        print("     |     |     ")
        print("  4  |  5  |  6  ")
        print("     |     |     ")
        print("-----+-----+-----")
        print("     |     |     ")
        print("  7  |  8  |  9  ")
        print("     |     |     ")
        print()
        print("-"*50)
        
    def is_valid_move(self, position):
        """Check if a move is valid"""
        return 0 <= position < 9 and self.board[position] == ' '
    
    def make_move(self, position):
        """Make a move on the board"""
        if self.is_valid_move(position):
            self.board[position] = self.current_player
            return True
        return False
    
    def get_available_positions(self):
        """Get list of available positions"""
        return [i for i in range(9) if self.board[i] == ' ']
    
    def check_winner(self):
        """Check if there's a winner"""
        # Winning combinations
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] 
                and self.board[combo[0]] != ' '):
                return self.board[combo[0]]
        return None
    
    def is_board_full(self):
        """Check if the board is full"""
        return ' ' not in self.board
    
    def switch_player(self):
        """Switch to the other player"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def reset(self):
        """Reset the game board"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'


class GameController:
    """Controls the game flow"""
    
    def __init__(self):
        """Initialize game controller"""
        self.game = TicTacToe()
        self.num_human_players = 2
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_title(self):
        """Display game title screen"""
        print("\n" + "="*50)
        print("||" + " "*46 + "||")
        print("||" + " "*12 + "TIC TAC TOE" + " "*23 + "||")
        print("||" + " "*46 + "||")
        print("||" + " "*10 + "~ 80's Edition ~" + " "*19 + "||")
        print("||" + " "*46 + "||")
        print("="*50)
        print()
        
    def get_player_mode(self):
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
    
    def get_human_move(self, player_symbol):
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
                    
                if not self.game.is_valid_move(position):
                    print("  ERROR: That position is already taken.")
                    continue
                    
                return position
                
            except (ValueError, KeyboardInterrupt):
                print("  ERROR: Invalid input.")
    
    def get_computer_move(self, player_symbol):
        """Get move from computer (random available position)"""
        available = self.game.get_available_positions()
        if available:
            position = random.choice(available)
            print(f"\n  Computer ({player_symbol}) is thinking...")
            print(f"  Computer selects position {position + 1}")
            input("  Press Enter to continue...")
            return position
        return None
    
    def play_game(self):
        """Main game loop"""
        self.game.reset()
        self.game.display_positions()
        
        while True:
            self.game.display_board()
            
            # Determine if current player is human or computer
            if self.game.current_player == 'X':
                is_human = self.num_human_players >= 1
            else:
                is_human = self.num_human_players == 2
            
            # Get and make move
            if is_human:
                position = self.get_human_move(self.game.current_player)
                self.game.make_move(position)
            else:
                position = self.get_computer_move(self.game.current_player)
                if position is not None:
                    self.game.make_move(position)
            
            # Check for winner
            winner = self.game.check_winner()
            if winner:
                self.game.display_board()
                print("\n" + "="*50)
                print(f"         Player {winner} WINS!")
                print("="*50)
                break
            
            # Check for draw
            if self.game.is_board_full():
                self.game.display_board()
                print("\n" + "="*50)
                print("         GAME DRAW!")
                print("="*50)
                break
            
            # Switch to next player
            self.game.switch_player()
    
    def play_again(self):
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
    
    def run(self):
        """Run the game application"""
        self.clear_screen()
        self.display_title()
        
        while True:
            self.num_human_players = self.get_player_mode()
            self.clear_screen()
            self.display_title()
            
            if self.num_human_players == 0:
                print("\n  Starting Computer vs Computer game...")
            elif self.num_human_players == 1:
                print("\n  Starting Human vs Computer game...")
                print("  You are Player X")
            else:
                print("\n  Starting Human vs Human game...")
            
            input("\n  Press Enter to start...")
            self.clear_screen()
            
            self.play_game()
            
            if not self.play_again():
                break
            
            self.clear_screen()
            self.display_title()
        
        print("\n" + "="*50)
        print("         Thank you for playing!")
        print("="*50)
        print()


def main():
    """Main entry point"""
    try:
        controller = GameController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n  ERROR: {e}\n")


if __name__ == "__main__":
    main()
