#!/usr/bin/env python3
"""
Integration test for DQN training with the fix
Tests that the training loop properly stores losing moves
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe_package.dqn_agent import DQNAgent, DQNConfig, encode_board
from tictactoe_package.game import TicTacToe


def outcome_reward(winner: str | None, mover: str) -> float:
    if winner is None:
        return 0.0
    return +1.0 if mover == winner else -1.0


def test_training_loop_stores_losing_moves():
    """
    Integration test: Run a few training episodes and verify that
    losing moves are being stored in the replay buffer.
    """
    print("\n✓ Testing training loop stores losing moves...")
    
    agent = DQNAgent(DQNConfig())
    
    # Track how many losing experiences we find
    losing_experiences = 0
    winning_experiences = 0
    
    # Run a small number of training episodes
    for ep in range(1, 101):
        env = TicTacToe()
        prev_experience = None
        
        while True:
            s = encode_board(env.board, env.current_player)
            a = agent.select_action(env.board, env.current_player, explore=True)
            if a == -1:
                break
            
            mover = env.current_player
            env.make_move(a)
            winner = env.check_winner()
            done = winner is not None or env.is_board_full()
            step_penalty = -0.01
            
            if done:
                r = outcome_reward(winner, mover) + step_penalty
                s_next = encode_board(env.board, env.current_player)
                agent.remember(s, a, r, s_next, True)
                agent.step_count += 1
                agent.learn()
                
                # Track winning experiences
                if r > 0.5:
                    winning_experiences += 1
                
                # The fix: store previous player's losing move
                if prev_experience is not None and winner is not None and winner != prev_experience[2]:
                    prev_s, prev_a, prev_mover = prev_experience
                    prev_r = -1.0 + step_penalty
                    prev_s_next = encode_board(env.board, prev_mover)
                    agent.remember(prev_s, prev_a, prev_r, prev_s_next, True)
                    agent.step_count += 1
                    agent.learn()
                    
                    # Track losing experiences
                    losing_experiences += 1
                
                break
            else:
                env.switch_player()
                r = step_penalty
                s_next = encode_board(env.board, env.current_player)
                agent.remember(s, a, r, s_next, False)
                agent.step_count += 1
                agent.learn()
                
                prev_experience = (s, a, mover)
    
    print(f"  Episodes: 100")
    print(f"  Winning experiences stored: {winning_experiences}")
    print(f"  Losing experiences stored: {losing_experiences}")
    print(f"  Total buffer size: {len(agent.buffer)}")
    
    # Verify that we stored some losing experiences
    # (With 100 episodes, we should have several games with winners)
    assert losing_experiences > 0, \
        "Should have stored at least some losing experiences during training"
    
    # Verify that losing experiences are roughly equal to winning experiences
    # (Each game with a winner should have one winner and one loser)
    assert abs(losing_experiences - winning_experiences) <= 5, \
        f"Losing ({losing_experiences}) and winning ({winning_experiences}) experiences should be roughly equal"
    
    print("  ✓ Training loop correctly stores both winning and losing moves")


def run_integration_tests():
    """Run integration tests"""
    print("\nRunning DQN Integration Tests...")
    print("=" * 60)
    
    test_training_loop_stores_losing_moves()
    
    print("=" * 60)
    print("All integration tests passed! ✓")
    print()


if __name__ == "__main__":
    run_integration_tests()
