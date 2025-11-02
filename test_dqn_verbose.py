#!/usr/bin/env python3
"""
Unit tests for the verbose parameter in DQN agent
"""

import sys
import os
from io import StringIO

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe_package.dqn_agent import DQNAgent, DQNConfig
from tictactoe_package.game import TicTacToe


def test_verbose_true_prints_why():
    """
    Test that when verbose=True, the agent prints the 'why' explanation
    """
    print("\n✓ Testing that verbose=True prints explanations...")
    
    # Create agent with verbose=True (default)
    cfg = DQNConfig()
    cfg.verbose = True
    agent = DQNAgent(cfg)
    
    # Create a simple board state
    env = TicTacToe()
    
    # Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured_output
    
    try:
        # Make a move (explore=False to trigger the verbose output)
        position = agent.select_action(env.board, env.current_player, explore=False)
        
        # Restore stdout
        sys.stdout = original_stdout
        
        # Get the output
        output = captured_output.getvalue()
        
        # Verify that the output contains the 'Why' explanation
        assert "[Why]" in output, f"Expected '[Why]' in output when verbose=True, got: {output}"
        assert "Top candidates:" in output, f"Expected 'Top candidates:' in output when verbose=True, got: {output}"
        
        print("  ✓ Verbose mode correctly prints explanations")
        
    except Exception as e:
        sys.stdout = original_stdout
        raise e


def test_verbose_false_no_print():
    """
    Test that when verbose=False, the agent does not print the 'why' explanation
    """
    print("\n✓ Testing that verbose=False suppresses explanations...")
    
    # Create agent with verbose=False
    cfg = DQNConfig()
    cfg.verbose = False
    agent = DQNAgent(cfg)
    
    # Create a simple board state
    env = TicTacToe()
    
    # Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured_output
    
    try:
        # Make a move (explore=False to ensure we go through the code path)
        position = agent.select_action(env.board, env.current_player, explore=False)
        
        # Restore stdout
        sys.stdout = original_stdout
        
        # Get the output
        output = captured_output.getvalue()
        
        # Verify that the output does NOT contain the 'Why' explanation
        assert "[Why]" not in output, f"Did not expect '[Why]' in output when verbose=False, got: {output}"
        assert "Top candidates:" not in output, f"Did not expect 'Top candidates:' in output when verbose=False, got: {output}"
        
        print("  ✓ Verbose mode correctly suppresses explanations")
        
    except Exception as e:
        sys.stdout = original_stdout
        raise e


def test_verbose_default_is_true():
    """
    Test that the default value of verbose is True
    """
    print("\n✓ Testing that verbose defaults to True...")
    
    # Create agent with default config
    cfg = DQNConfig()
    
    # Verify that verbose is True by default
    assert cfg.verbose is True, f"Expected verbose to default to True, got {cfg.verbose}"
    
    print("  ✓ Default verbose value is True")


def test_pick_move_respects_verbose():
    """
    Test that pick_move (which calls select_action with explore=False) respects verbose setting
    """
    print("\n✓ Testing that pick_move respects verbose setting...")
    
    # Test with verbose=False
    cfg = DQNConfig()
    cfg.verbose = False
    agent = DQNAgent(cfg)
    
    env = TicTacToe()
    
    # Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured_output
    
    try:
        # Call pick_move (used during gameplay)
        position = agent.pick_move(env.board, env.current_player)
        
        # Restore stdout
        sys.stdout = original_stdout
        
        # Get the output
        output = captured_output.getvalue()
        
        # Verify no output when verbose=False
        assert "[Why]" not in output, f"pick_move should respect verbose=False"
        
        print("  ✓ pick_move respects verbose setting")
        
    except Exception as e:
        sys.stdout = original_stdout
        raise e


def test_multiple_moves_with_verbose():
    """
    Test that verbose setting works correctly across multiple moves
    """
    print("\n✓ Testing verbose setting across multiple moves...")
    
    # Test with verbose=True
    cfg_verbose = DQNConfig()
    cfg_verbose.verbose = True
    agent_verbose = DQNAgent(cfg_verbose)
    
    # Test with verbose=False
    cfg_silent = DQNConfig()
    cfg_silent.verbose = False
    agent_silent = DQNAgent(cfg_silent)
    
    env = TicTacToe()
    
    # Make multiple moves and count outputs
    verbose_output_count = 0
    silent_output_count = 0
    
    original_stdout = sys.stdout
    
    try:
        for i in range(3):
            # Verbose agent
            captured = StringIO()
            sys.stdout = captured
            agent_verbose.select_action(env.board, env.current_player, explore=False)
            sys.stdout = original_stdout
            if "[Why]" in captured.getvalue():
                verbose_output_count += 1
            
            # Silent agent
            captured = StringIO()
            sys.stdout = captured
            agent_silent.select_action(env.board, env.current_player, explore=False)
            sys.stdout = original_stdout
            if "[Why]" in captured.getvalue():
                silent_output_count += 1
        
        assert verbose_output_count == 3, f"Expected 3 verbose outputs, got {verbose_output_count}"
        assert silent_output_count == 0, f"Expected 0 verbose outputs, got {silent_output_count}"
        
        print("  ✓ Verbose setting works correctly across multiple moves")
        
    finally:
        sys.stdout = original_stdout


def run_all_tests():
    """Run all verbose parameter tests"""
    print("\nRunning DQN Verbose Parameter Tests...")
    print("=" * 60)
    
    test_verbose_default_is_true()
    test_verbose_true_prints_why()
    test_verbose_false_no_print()
    test_pick_move_respects_verbose()
    test_multiple_moves_with_verbose()
    
    print("=" * 60)
    print("All verbose parameter tests passed! ✓")
    print()


if __name__ == "__main__":
    run_all_tests()
