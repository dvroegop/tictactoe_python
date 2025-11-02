"""
User interface functions for TicTacToe
Handles display and formatting of game elements
"""

import os


class GameUI:
    """Handles all UI display logic"""
    
    # ANSI color codes for high-visibility presentation
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Bright colors for presentation visibility
    CYAN = '\033[96m'       # Bright cyan for X
    YELLOW = '\033[93m'     # Bright yellow for O
    GREEN = '\033[92m'      # Bright green for titles
    WHITE = '\033[97m'      # Bright white for grid
    BLUE = '\033[94m'       # Bright blue for borders
    MAGENTA = '\033[95m'    # Bright magenta for highlights
    
    # Cursor control codes
    CLEAR_LINE = '\033[2K'
    MOVE_UP = '\033[F'
    
    # Board display constants
    BOARD_AREA_LINES = 18  # Number of lines reserved for board display
    
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def display_title():
        """Display game title screen"""
        print("\n" + GameUI.BLUE + GameUI.BOLD + "="*50 + GameUI.RESET)
        print(GameUI.BLUE + "||" + " "*46 + "||" + GameUI.RESET)
        print(GameUI.BLUE + "||" + " "*12 + GameUI.GREEN + GameUI.BOLD + "TIC TAC TOE" + GameUI.BLUE + " "*23 + "||" + GameUI.RESET)
        print(GameUI.BLUE + "||" + " "*46 + "||" + GameUI.RESET)
        print(GameUI.BLUE + "||" + " "*10 + GameUI.MAGENTA + "~ 80's Edition ~" + GameUI.BLUE + " "*19 + "||" + GameUI.RESET)
        print(GameUI.BLUE + "||" + " "*46 + "||" + GameUI.RESET)
        print(GameUI.BLUE + GameUI.BOLD + "="*50 + GameUI.RESET)
        print()
    
    @staticmethod
    def display_board(board):
        """Display the game board with 80's style formatting and colors
        Uses ANSI codes to stay in fixed position"""
        
        # Helper function to colorize symbols
        def colorize(symbol):
            if symbol == 'X':
                return f"{GameUI.CYAN}{GameUI.BOLD}{symbol}{GameUI.RESET}"
            elif symbol == 'O':
                return f"{GameUI.YELLOW}{GameUI.BOLD}{symbol}{GameUI.RESET}"
            else:
                return f"{GameUI.WHITE}{symbol}{GameUI.RESET}"
        
        # Clear the board area
        for _ in range(GameUI.BOARD_AREA_LINES):
            print(GameUI.CLEAR_LINE)
            
        # Move cursor back up to start of board area
        print(GameUI.MOVE_UP * GameUI.BOARD_AREA_LINES, end='')
        
        # Display the board
        print(GameUI.BLUE + GameUI.BOLD + "="*50 + GameUI.RESET)
        print(GameUI.GREEN + GameUI.BOLD + "                  TIC TAC TOE" + GameUI.RESET)
        print(GameUI.BLUE + GameUI.BOLD + "="*50 + GameUI.RESET)
        print()
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(f"  {colorize(board[0])}  {GameUI.WHITE}|{GameUI.RESET}  {colorize(board[1])}  {GameUI.WHITE}|{GameUI.RESET}  {colorize(board[2])}  ")
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(GameUI.WHITE + "-----+-----+-----" + GameUI.RESET)
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(f"  {colorize(board[3])}  {GameUI.WHITE}|{GameUI.RESET}  {colorize(board[4])}  {GameUI.WHITE}|{GameUI.RESET}  {colorize(board[5])}  ")
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(GameUI.WHITE + "-----+-----+-----" + GameUI.RESET)
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(f"  {colorize(board[6])}  {GameUI.WHITE}|{GameUI.RESET}  {colorize(board[7])}  {GameUI.WHITE}|{GameUI.RESET}  {colorize(board[8])}  ")
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print()
        print(GameUI.BLUE + GameUI.BOLD + "="*50 + GameUI.RESET)
    
    @staticmethod
    def display_positions():
        """Display position numbers for reference"""
        print("\n" + GameUI.MAGENTA + GameUI.BOLD + "-"*50 + GameUI.RESET)
        print(GameUI.MAGENTA + GameUI.BOLD + "         Position Reference:" + GameUI.RESET)
        print(GameUI.MAGENTA + GameUI.BOLD + "-"*50 + GameUI.RESET)
        print()
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(GameUI.WHITE + "  1  |  2  |  3  " + GameUI.RESET)
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(GameUI.WHITE + "-----+-----+-----" + GameUI.RESET)
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(GameUI.WHITE + "  4  |  5  |  6  " + GameUI.RESET)
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(GameUI.WHITE + "-----+-----+-----" + GameUI.RESET)
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print(GameUI.WHITE + "  7  |  8  |  9  " + GameUI.RESET)
        print(GameUI.WHITE + "     |     |     " + GameUI.RESET)
        print()
        print(GameUI.MAGENTA + GameUI.BOLD + "-"*50 + GameUI.RESET)
    
    @staticmethod
    def display_winner(winner):
        """Display winner message"""
        print("\n" + GameUI.GREEN + GameUI.BOLD + "="*50 + GameUI.RESET)
        print(GameUI.GREEN + GameUI.BOLD + f"         Player {winner} WINS!" + GameUI.RESET)
        print(GameUI.GREEN + GameUI.BOLD + "="*50 + GameUI.RESET)
    
    @staticmethod
    def display_draw():
        """Display draw message"""
        print("\n" + GameUI.YELLOW + GameUI.BOLD + "="*50 + GameUI.RESET)
        print(GameUI.YELLOW + GameUI.BOLD + "         GAME DRAW!" + GameUI.RESET)
        print(GameUI.YELLOW + GameUI.BOLD + "="*50 + GameUI.RESET)
    
    @staticmethod
    def display_goodbye():
        """Display goodbye message"""
        print("\n" + GameUI.BLUE + GameUI.BOLD + "="*50 + GameUI.RESET)
        print(GameUI.GREEN + GameUI.BOLD + "         Thank you for playing!" + GameUI.RESET)
        print(GameUI.BLUE + GameUI.BOLD + "="*50 + GameUI.RESET)
        print()
    
    @staticmethod
    def prepare_board_area():
        """Prepare space for the board display (reserve lines)"""
        # Print empty lines for the board area
        for _ in range(GameUI.BOARD_AREA_LINES):
            print()
        # Move cursor back to start of board area
        print(GameUI.MOVE_UP * GameUI.BOARD_AREA_LINES, end='')
