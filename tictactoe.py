#!/usr/bin/env python3
"""
TicTacToe Game - Console Edition
Inspired by 80's style computer games

Main entry point for the game.
"""

from tictactoe_package import GameController

# Keep the old imports for backward compatibility
from tictactoe_package import TicTacToe


def main():
    """Main entry point"""
    try:
        controller = GameController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n  ERROR: {e}\n")


if __name__ == "__main__":
    main()
