#!/usr/bin/env python3
"""
Tests for RL Agent with player-aware state representation
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe_package.rl_agent import RLAgent, board_to_state


def test_board_to_state_includes_player():
    """Test that board_to_state includes the current player"""
    board = ['X', ' ', 'O', ' ', 'X', ' ', ' ', ' ', ' ']
    
    # Test with X as current player
    state_x = board_to_state(board, 'X')
    assert '|X' in state_x, "State should contain |X for player X"
    
    # Test with O as current player
    state_o = board_to_state(board, 'O')
    assert '|O' in state_o, "State should contain |O for player O"
    
    # States should be different for same board but different players
    assert state_x != state_o, "States should differ when player differs"
    
    print("✓ board_to_state includes player test passed")


def test_board_to_state_format():
    """Test the exact format of board_to_state"""
    board = ['X', ' ', 'O', ' ', 'X', ' ', ' ', ' ', ' ']
    
    state_x = board_to_state(board, 'X')
    expected_x = "X O X    |X"
    assert state_x == expected_x, f"Expected '{expected_x}', got '{state_x}'"
    
    state_o = board_to_state(board, 'O')
    expected_o = "X O X    |O"
    assert state_o == expected_o, f"Expected '{expected_o}', got '{state_o}'"
    
    print("✓ board_to_state format test passed")


def test_rl_agent_pick_move_with_player():
    """Test that pick_move accepts current_player parameter"""
    agent = RLAgent()
    board = [' '] * 9
    
    # Should work with X as current player
    move_x = agent.pick_move(board, 'X')
    assert 0 <= move_x < 9, "Move should be valid"
    
    # Should work with O as current player
    move_o = agent.pick_move(board, 'O')
    assert 0 <= move_o < 9, "Move should be valid"
    
    print("✓ RL agent pick_move with player test passed")


def test_rl_agent_training_creates_player_aware_states():
    """Test that training creates states with player information"""
    agent = RLAgent()
    
    # Train for just a few episodes
    agent.train_self_play(episodes=10)
    
    # Check that Q-table has player-aware states
    has_x_states = False
    has_o_states = False
    
    for (state, action) in agent.q.keys():
        if '|X' in state:
            has_x_states = True
        if '|O' in state:
            has_o_states = True
    
    assert has_x_states, "Training should create states for player X"
    assert has_o_states, "Training should create states for player O"
    
    print("✓ RL agent training creates player-aware states test passed")


def test_rl_agent_same_board_different_players():
    """Test that agent can distinguish same board with different players"""
    agent = RLAgent()
    
    # Train briefly
    agent.train_self_play(episodes=100)
    
    # Create a simple board state
    board = ['X', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    
    # Get Q-values for the same board but different players
    state_x = board_to_state(board, 'X')
    state_o = board_to_state(board, 'O')
    
    # Make some moves to populate Q-table
    legal = [i for i, v in enumerate(board) if v == ' ']
    
    # The states should be different
    assert state_x != state_o, "States should be different for different players"
    
    # Both states should be valid for querying
    q_x = agent.value(state_x, legal[0])
    q_o = agent.value(state_o, legal[0])
    
    # Q-values are initially 0.0 or learned values - both are valid
    assert isinstance(q_x, float), "Q-value for X should be a float"
    assert isinstance(q_o, float), "Q-value for O should be a float"
    
    print("✓ RL agent distinguishes same board with different players test passed")


def test_rl_agent_save_load_with_player_states():
    """Test that Q-table can be saved and loaded with player-aware states"""
    import tempfile
    import os
    
    agent1 = RLAgent()
    
    # Train briefly
    agent1.train_self_play(episodes=50)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = f.name
    
    try:
        agent1.save(temp_path)
        
        # Create new agent and load
        agent2 = RLAgent()
        agent2.load(temp_path)
        
        # Check that Q-tables match
        assert len(agent1.q) == len(agent2.q), "Q-table sizes should match"
        
        # Check a few random entries
        for key in list(agent1.q.keys())[:5]:
            assert key in agent2.q, f"Key {key} should be in loaded Q-table"
            assert abs(agent1.q[key] - agent2.q[key]) < 1e-6, "Q-values should match"
        
        print("✓ RL agent save/load with player states test passed")
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def run_all_tests():
    """Run all RL agent tests"""
    print("\nRunning RL Agent tests...")
    print("=" * 50)
    
    test_board_to_state_includes_player()
    test_board_to_state_format()
    test_rl_agent_pick_move_with_player()
    test_rl_agent_training_creates_player_aware_states()
    test_rl_agent_same_board_different_players()
    test_rl_agent_save_load_with_player_states()
    
    print("=" * 50)
    print("All RL agent tests passed! ✓")
    print()


if __name__ == "__main__":
    run_all_tests()
