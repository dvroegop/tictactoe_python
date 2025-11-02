#!/usr/bin/env python3
"""
TicTacToe Game - Console Edition
Inspired by 80's style computer games

Main entry point for the game.
"""

import sys
from tictactoe_package import GameController

# Keep the old imports for backward compatibility
from tictactoe_package import TicTacToe


def main():
    """Main entry point"""
    try:
        # Parse command line arguments
        auto_mode = False
        num_games = 50  # Default number of games
        
        if len(sys.argv) > 1:
            if sys.argv[1] == '-auto':
                auto_mode = True
                # Check if a number is provided after -auto
                if len(sys.argv) > 2:
                    try:
                        num_games = int(sys.argv[2])
                        if num_games <= 0:
                            print("Error: Number of games must be positive")
                            sys.exit(1)
                    except ValueError:
                        print(f"Error: Invalid number of games: {sys.argv[2]}")
                        sys.exit(1)
        
        controller = GameController()
        
        if auto_mode:
            controller.run_auto(num_games)
        else:
            controller.run()
            
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n  ERROR: {e}\n")


if __name__ == "__main__":
    main()
