#!/usr/bin/env python3
"""
Simple tests for TicTacToe game
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe import TicTacToe, GameController


def test_board_initialization():
    """Test that board initializes correctly"""
    game = TicTacToe()
    assert game.board == [' '] * 9, "Board should be empty initially"
    assert game.current_player == 'X', "X should start first"
    print("✓ Board initialization test passed")


def test_valid_move():
    """Test making valid moves"""
    game = TicTacToe()
    assert game.make_move(0) == True, "Should allow move on empty position"
    assert game.board[0] == 'X', "Board should update with player's mark"
    assert game.make_move(0) == False, "Should not allow move on occupied position"
    print("✓ Valid move test passed")


def test_is_valid_move():
    """Test move validation"""
    game = TicTacToe()
    assert game.is_valid_move(0) == True, "Empty position should be valid"
    game.board[0] = 'X'
    assert game.is_valid_move(0) == False, "Occupied position should be invalid"
    assert game.is_valid_move(-1) == False, "Negative position should be invalid"
    assert game.is_valid_move(9) == False, "Position > 8 should be invalid"
    print("✓ Move validation test passed")


def test_available_positions():
    """Test getting available positions"""
    game = TicTacToe()
    assert len(game.get_available_positions()) == 9, "All positions should be available initially"
    game.board[0] = 'X'
    game.board[4] = 'O'
    available = game.get_available_positions()
    assert len(available) == 7, "Should have 7 available positions"
    assert 0 not in available, "Occupied position should not be available"
    assert 4 not in available, "Occupied position should not be available"
    print("✓ Available positions test passed")


def test_winner_detection_row():
    """Test winner detection for rows"""
    game = TicTacToe()
    # Test first row
    game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
    assert game.check_winner() == 'X', "Should detect winner in first row"
    
    # Test second row
    game.board = [' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ']
    assert game.check_winner() == 'O', "Should detect winner in second row"
    
    # Test third row
    game.board = [' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'X']
    assert game.check_winner() == 'X', "Should detect winner in third row"
    print("✓ Row winner detection test passed")


def test_winner_detection_column():
    """Test winner detection for columns"""
    game = TicTacToe()
    # Test first column
    game.board = ['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ']
    assert game.check_winner() == 'X', "Should detect winner in first column"
    
    # Test second column
    game.board = [' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O', ' ']
    assert game.check_winner() == 'O', "Should detect winner in second column"
    
    # Test third column
    game.board = [' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X']
    assert game.check_winner() == 'X', "Should detect winner in third column"
    print("✓ Column winner detection test passed")


def test_winner_detection_diagonal():
    """Test winner detection for diagonals"""
    game = TicTacToe()
    # Test top-left to bottom-right diagonal
    game.board = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
    assert game.check_winner() == 'X', "Should detect winner in main diagonal"
    
    # Test top-right to bottom-left diagonal
    game.board = [' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ']
    assert game.check_winner() == 'O', "Should detect winner in anti-diagonal"
    print("✓ Diagonal winner detection test passed")


def test_no_winner():
    """Test no winner detection"""
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'X', 'O', 'X', 'O']
    assert game.check_winner() is None, "Should detect no winner"
    print("✓ No winner detection test passed")


def test_board_full():
    """Test board full detection"""
    game = TicTacToe()
    assert game.is_board_full() == False, "Empty board should not be full"
    game.board = ['X', 'O', 'X', 'O', 'X', 'X', 'O', 'X', 'O']
    assert game.is_board_full() == True, "Full board should be detected"
    print("✓ Board full detection test passed")


def test_player_switching():
    """Test player switching"""
    game = TicTacToe()
    assert game.current_player == 'X', "Should start with X"
    game.switch_player()
    assert game.current_player == 'O', "Should switch to O"
    game.switch_player()
    assert game.current_player == 'X', "Should switch back to X"
    print("✓ Player switching test passed")


def test_board_reset():
    """Test board reset"""
    game = TicTacToe()
    game.board = ['X', 'O', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
    game.current_player = 'O'
    game.reset()
    assert game.board == [' '] * 9, "Board should be reset"
    assert game.current_player == 'X', "Current player should reset to X"
    print("✓ Board reset test passed")


def run_all_tests():
    """Run all tests"""
    print("\nRunning TicTacToe tests...")
    print("=" * 50)
    
    test_board_initialization()
    test_valid_move()
    test_is_valid_move()
    test_available_positions()
    test_winner_detection_row()
    test_winner_detection_column()
    test_winner_detection_diagonal()
    test_no_winner()
    test_board_full()
    test_player_switching()
    test_board_reset()
    
    print("=" * 50)
    print("All tests passed! ✓")
    print()


if __name__ == "__main__":
    run_all_tests()
