#!/usr/bin/env python3
"""
Test DQN agent against a smart opponent that blocks and tries to win
This simulates a human player better than pure random
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe_package.dqn_agent import DQNAgent, DQNConfig
from tictactoe_package.game import TicTacToe
import random


def check_winning_move(board, player):
    """Check if there's a winning move for the player"""
    for pos in range(9):
        if board[pos] == ' ':
            # Try the move
            board[pos] = player
            game = TicTacToe()
            game.board = board.copy()
            if game.check_winner() == player:
                board[pos] = ' '  # Undo
                return pos
            board[pos] = ' '  # Undo
    return None


def smart_opponent_move(board, opponent_mark):
    """
    Smart opponent strategy:
    1. Win if possible
    2. Block opponent from winning
    3. Take center if available
    4. Take corner
    5. Random
    """
    # 1. Check if we can win
    winning_move = check_winning_move(board, opponent_mark)
    if winning_move is not None:
        return winning_move
    
    # 2. Check if we need to block opponent
    player_mark = 'X' if opponent_mark == 'O' else 'O'
    blocking_move = check_winning_move(board, player_mark)
    if blocking_move is not None:
        return blocking_move
    
    # 3. Take center if available
    if board[4] == ' ':
        return 4
    
    # 4. Take a corner
    corners = [0, 2, 6, 8]
    available_corners = [c for c in corners if board[c] == ' ']
    if available_corners:
        return random.choice(available_corners)
    
    # 5. Take any available space
    available = [i for i in range(9) if board[i] == ' ']
    return random.choice(available) if available else None


def play_game_dqn_vs_smart(agent, dqn_player='X'):
    """Play a game where DQN plays against a smart opponent"""
    env = TicTacToe()
    
    while True:
        available = env.get_available_positions()
        if not available:
            break
        
        # Choose move based on current player
        if env.current_player == dqn_player:
            # DQN's turn
            position = agent.pick_move(env.board, env.current_player)
            if position not in available:
                position = random.choice(available)
        else:
            # Smart opponent's turn
            opponent_mark = env.current_player
            position = smart_opponent_move(env.board, opponent_mark)
        
        env.make_move(position)
        winner = env.check_winner()
        
        if winner or env.is_board_full():
            return winner
        
        env.switch_player()
    
    return None


def evaluate_against_smart_opponent(policy_path="dqn_policy.pt"):
    """Evaluate the trained DQN agent against a smart opponent"""
    print("\n" + "=" * 60)
    print("Evaluating DQN Agent vs Smart Opponent")
    print("=" * 60)
    
    # Load trained agent
    cfg = DQNConfig()
    cfg.verbose = False  # Disable verbose output during evaluation for cleaner results
    agent = DQNAgent(cfg)
    try:
        agent.load(policy_path)
        print(f"✓ Loaded policy from {policy_path}")
    except Exception as e:
        print(f"✗ Could not load policy: {e}")
        return
    
    # Test 1: DQN as X vs Smart opponent
    print("\n--- Test 1: DQN (as X) vs Smart Opponent (100 games) ---")
    results = {'X': 0, 'O': 0, 'Draw': 0}
    
    for _ in range(100):
        winner = play_game_dqn_vs_smart(agent, dqn_player='X')
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1
    
    print(f"DQN (X) wins: {results['X']}")
    print(f"Smart (O) wins (DQN losses): {results['O']}")
    print(f"Draws: {results['Draw']}")
    print(f"DQN win/draw rate: {(results['X'] + results['Draw'])}%")
    
    # Test 2: DQN as O vs Smart opponent
    print("\n--- Test 2: Smart Opponent (as X) vs DQN (100 games) ---")
    results = {'X': 0, 'O': 0, 'Draw': 0}
    
    for _ in range(100):
        winner = play_game_dqn_vs_smart(agent, dqn_player='O')
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1
    
    print(f"Smart (X) wins (DQN losses): {results['X']}")
    print(f"DQN (O) wins: {results['O']}")
    print(f"Draws: {results['Draw']}")
    print(f"DQN win/draw rate: {(results['O'] + results['Draw'])}%")
    
    print("\n" + "=" * 60)
    print("Evaluation Complete!")
    print("=" * 60)
    print("\nExpected Results Against Smart Opponent:")
    print("- Should have many draws (40%+)")
    print("- Should rarely lose (< 30%)")
    print("- The fix ensures DQN learns from losing positions")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import sys
    policy_path = sys.argv[1] if len(sys.argv) > 1 else "dqn_policy.pt"
    evaluate_against_smart_opponent(policy_path)
