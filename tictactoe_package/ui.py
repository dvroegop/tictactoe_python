"""
User interface functions for TicTacToe
Handles display and formatting of game elements
"""

import os


class GameUI:
    """Handles all UI display logic"""
    
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def display_title():
        """Display game title screen"""
        print("\n" + "="*50)
        print("||" + " "*46 + "||")
        print("||" + " "*12 + "TIC TAC TOE" + " "*23 + "||")
        print("||" + " "*46 + "||")
        print("||" + " "*10 + "~ 80's Edition ~" + " "*19 + "||")
        print("||" + " "*46 + "||")
        print("="*50)
        print()
    
    @staticmethod
    def display_board(board):
        """Display the game board with 80's style formatting"""
        print("\n" + "="*50)
        print("                  TIC TAC TOE")
        print("="*50)
        print()
        print("     |     |     ")
        print(f"  {board[0]}  |  {board[1]}  |  {board[2]}  ")
        print("     |     |     ")
        print("-----+-----+-----")
        print("     |     |     ")
        print(f"  {board[3]}  |  {board[4]}  |  {board[5]}  ")
        print("     |     |     ")
        print("-----+-----+-----")
        print("     |     |     ")
        print(f"  {board[6]}  |  {board[7]}  |  {board[8]}  ")
        print("     |     |     ")
        print()
        print("="*50)
    
    @staticmethod
    def display_positions():
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
    
    @staticmethod
    def display_winner(winner):
        """Display winner message"""
        print("\n" + "="*50)
        print(f"         Player {winner} WINS!")
        print("="*50)
    
    @staticmethod
    def display_draw():
        """Display draw message"""
        print("\n" + "="*50)
        print("         GAME DRAW!")
        print("="*50)
    
    @staticmethod
    def display_goodbye():
        """Display goodbye message"""
        print("\n" + "="*50)
        print("         Thank you for playing!")
        print("="*50)
        print()
