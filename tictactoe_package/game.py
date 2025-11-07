"""
Core game logic for TicTacToe
Handles board state, move validation, and winner detection
"""


class TicTacToe:
    """Main TicTacToe game class"""
    
    def __init__(self):
        """Initialize the game board"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        
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
