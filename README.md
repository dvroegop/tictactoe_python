# TicTacToe - 80's Edition

A console-based TicTacToe game inspired by Wargames and classic 80's computer games.

## Features

- **3 Game Modes:**
  - Human vs Human (2 players)
  - Human vs Computer (1 player)
  - Computer vs Computer (0 players - watch the AI play!)

- **Classic 80's Style:**
  - Fixed-width console display
  - Retro ASCII graphics
  - Simple and intuitive interface

- **Smart AI:**
  - Computer opponent plays randomly on available cells
  - Perfect for casual gameplay

## How to Play

1. **Run the game:**
   ```bash
   python3 tictactoe.py
   ```

2. **Select game mode:**
   - Enter `0` for Computer vs Computer
   - Enter `1` for Human vs Computer (you play as X)
   - Enter `2` for Human vs Human

3. **Make your move:**
   - Enter a number from 1-9 to place your mark
   - The position reference shows which number corresponds to which cell:
     ```
     1 | 2 | 3
     ---------
     4 | 5 | 6
     ---------
     7 | 8 | 9
     ```

4. **Win the game:**
   - Get three in a row (horizontal, vertical, or diagonal) to win!
   - If all cells are filled with no winner, it's a draw

## Requirements

- Python 3.6 or higher
- No external dependencies required!

## Example Game

```
==================================================
                  TIC TAC TOE
==================================================

     |     |     
  X  |  O  |  X  
     |     |     
-----+-----+-----
     |     |     
  O  |  X  |     
     |     |     
-----+-----+-----
     |     |     
     |     |     
     |     |     

==================================================
```

## Future Enhancements

This project is designed as a foundation for teaching Reinforcement Learning AI. Future versions may include:
- Smarter AI using reinforcement learning
- Training mode for AI
- Statistics tracking
- Different difficulty levels

## License

See LICENSE file for details.
