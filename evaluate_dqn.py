#!/usr/bin/env python3
"""
Evaluate DQN agent performance by playing games against itself and random opponent
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe_package.dqn_agent import DQNAgent, DQNConfig
from tictactoe_package.game import TicTacToe
import random


def play_game_dqn_vs_dqn(agent):
    """Play a game where DQN agent plays both sides"""
    env = TicTacToe()
    
    while True:
        # Get available positions
        available = env.get_available_positions()
        if not available:
            break
        
        # DQN picks move
        position = agent.pick_move(env.board, env.current_player)
        if position not in available:
            position = random.choice(available)
        
        env.make_move(position)
        winner = env.check_winner()
        
        if winner or env.is_board_full():
            return winner
        
        env.switch_player()
    
    return None


def play_game_dqn_vs_random(agent, dqn_player='X'):
    """Play a game where DQN plays one side and random plays the other"""
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
            # Random opponent's turn
            position = random.choice(available)
        
        env.make_move(position)
        winner = env.check_winner()
        
        if winner or env.is_board_full():
            return winner
        
        env.switch_player()
    
    return None


def evaluate_dqn_agent(policy_path="dqn_policy.pt"):
    """Evaluate the trained DQN agent"""
    print("\n" + "=" * 60)
    print("Evaluating DQN Agent Performance")
    print("=" * 60)
    
    # Load trained agent
    agent = DQNAgent(DQNConfig())
    try:
        agent.load(policy_path)
        print(f"✓ Loaded policy from {policy_path}")
    except Exception as e:
        print(f"✗ Could not load policy: {e}")
        return
    
    # Test 1: DQN vs DQN (should mostly draw since both play optimally)
    print("\n--- Test 1: DQN vs DQN (100 games) ---")
    results = {'X': 0, 'O': 0, 'Draw': 0}
    
    for _ in range(100):
        winner = play_game_dqn_vs_dqn(agent)
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1
    
    print(f"X wins: {results['X']}")
    print(f"O wins: {results['O']}")
    print(f"Draws: {results['Draw']}")
    print(f"Draw rate: {results['Draw']}%")
    
    # Test 2: DQN as X vs Random (DQN should win or draw most games)
    print("\n--- Test 2: DQN (as X) vs Random (100 games) ---")
    results = {'X': 0, 'O': 0, 'Draw': 0}
    
    for _ in range(100):
        winner = play_game_dqn_vs_random(agent, dqn_player='X')
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1
    
    print(f"DQN (X) wins: {results['X']}")
    print(f"Random (O) wins: {results['O']}")
    print(f"Draws: {results['Draw']}")
    print(f"DQN win/draw rate: {(results['X'] + results['Draw'])}%")
    
    # Test 3: DQN as O vs Random (DQN should win or draw most games)
    print("\n--- Test 3: Random (as X) vs DQN (100 games) ---")
    results = {'X': 0, 'O': 0, 'Draw': 0}
    
    for _ in range(100):
        winner = play_game_dqn_vs_random(agent, dqn_player='O')
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1
    
    print(f"Random (X) wins: {results['X']}")
    print(f"DQN (O) wins: {results['O']}")
    print(f"Draws: {results['Draw']}")
    print(f"DQN win/draw rate: {(results['O'] + results['Draw'])}%")
    
    print("\n" + "=" * 60)
    print("Evaluation Complete!")
    print("=" * 60)
    print("\nExpected Results:")
    print("- DQN vs DQN: High draw rate (70-90%)")
    print("- DQN vs Random: High win/draw rate (85-100%)")
    print("- If DQN loses frequently, training may need improvement")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    evaluate_dqn_agent()
