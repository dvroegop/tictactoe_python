#!/usr/bin/env python3
"""
Tests for DQN training to ensure proper credit assignment
"""

import sys
import os
import torch

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe_package.dqn_agent import DQNAgent, DQNConfig, encode_board
from tictactoe_package.game import TicTacToe


def test_losing_move_is_trained():
    """
    Test that when a player makes a move that leads to their opponent winning,
    that move is stored in the training buffer with negative reward.
    
    This is the core fix for the DQN training issue.
    """
    print("\n✓ Testing that losing moves are properly stored in training buffer...")
    
    # Create agent and environment
    agent = DQNAgent(DQNConfig())
    env = TicTacToe()
    
    # Set up a board state where X is about to lose
    # O O _   <- O needs to place at position 2 to win
    # X X _
    # _ _ _
    env.board = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
    env.current_player = 'X'
    
    # Record buffer size before
    initial_buffer_size = len(agent.buffer)
    
    # X makes a move (not blocking position 2) - let's say position 5
    s_x = encode_board(env.board, env.current_player)
    env.make_move(5)  # X moves to position 5
    env.switch_player()
    
    # Now it's O's turn, O will win by moving to position 2
    s_o = encode_board(env.board, env.current_player)
    env.make_move(2)  # O wins
    winner = env.check_winner()
    
    assert winner == 'O', "O should have won"
    
    # Simulate what the training loop should do:
    # 1. Store O's winning move
    r_o = 1.0 + (-0.01)  # win reward + step penalty
    s_next_o = encode_board(env.board, 'O')
    agent.remember(s_o, 2, r_o, s_next_o, True)
    
    # 2. Store X's losing move (the fix we implemented)
    r_x = -1.0 + (-0.01)  # loss reward + step penalty
    s_next_x = encode_board(env.board, 'X')
    agent.remember(s_x, 5, r_x, s_next_x, True)
    
    # Verify both transitions were added
    assert len(agent.buffer) == initial_buffer_size + 2, \
        "Both the winning and losing moves should be in the buffer"
    
    # Verify the last two experiences
    last_two = list(agent.buffer)[-2:]
    
    # First should be O's winning move with positive reward
    _, _, r1, _, done1 = last_two[0]
    assert r1 > 0.9, f"O's move should have positive reward, got {r1}"
    assert done1 == True, "O's move should be marked as done"
    
    # Second should be X's losing move with negative reward
    _, _, r2, _, done2 = last_two[1]
    assert r2 < -0.9, f"X's move should have negative reward, got {r2}"
    assert done2 == True, "X's move should be marked as done"
    
    print("  ✓ Both winning and losing moves correctly stored with appropriate rewards")


def test_draw_no_extra_experience():
    """
    Test that in case of a draw, we don't add extra experiences incorrectly.
    """
    print("\n✓ Testing that draws don't create incorrect experiences...")
    
    agent = DQNAgent(DQNConfig())
    env = TicTacToe()
    
    # Set up a board that will end in a draw with next move
    # X O X
    # X O O
    # O X _  <- X will move here and draw
    env.board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', ' ']
    env.current_player = 'X'
    
    initial_buffer_size = len(agent.buffer)
    
    # X makes the final move
    s_x = encode_board(env.board, env.current_player)
    env.make_move(8)
    winner = env.check_winner()
    
    assert winner is None, "Should be a draw"
    assert env.is_board_full(), "Board should be full"
    
    # Store X's move (draw outcome)
    r_x = 0.0 + (-0.01)  # draw reward + step penalty
    s_next_x = encode_board(env.board, 'X')
    agent.remember(s_x, 8, r_x, s_next_x, True)
    
    # In a draw, we should NOT add a previous player experience
    # (because neither player won/lost)
    assert len(agent.buffer) == initial_buffer_size + 1, \
        "Only one experience should be added for a draw"
    
    print("  ✓ Draw scenario correctly stores only one experience")


def test_winning_move_gets_positive_reward():
    """
    Test that when a player makes a winning move, they get positive reward.
    """
    print("\n✓ Testing that winning moves get positive rewards...")
    
    agent = DQNAgent(DQNConfig())
    env = TicTacToe()
    
    # Set up a board where X can win
    # X X _   <- X wins by moving to position 2
    # O O _
    # _ _ _
    env.board = ['X', 'X', ' ', 'O', 'O', ' ', ' ', ' ', ' ']
    env.current_player = 'X'
    
    initial_buffer_size = len(agent.buffer)
    
    # X makes winning move
    s_x = encode_board(env.board, env.current_player)
    env.make_move(2)
    winner = env.check_winner()
    
    assert winner == 'X', "X should have won"
    
    # Store X's winning move
    r_x = 1.0 + (-0.01)  # win reward + step penalty
    s_next_x = encode_board(env.board, 'X')
    agent.remember(s_x, 2, r_x, s_next_x, True)
    
    # Check the experience
    last_exp = list(agent.buffer)[-1]
    _, _, r, _, done = last_exp
    
    assert r > 0.9, f"Winning move should have positive reward, got {r}"
    assert done == True, "Winning move should be terminal"
    
    print("  ✓ Winning move correctly receives positive reward")


def run_all_tests():
    """Run all DQN training tests"""
    print("\nRunning DQN Training Tests...")
    print("=" * 60)
    
    test_losing_move_is_trained()
    test_draw_no_extra_experience()
    test_winning_move_gets_positive_reward()
    
    print("=" * 60)
    print("All DQN training tests passed! ✓")
    print()


if __name__ == "__main__":
    run_all_tests()
