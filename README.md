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

- **Two AI Options:**
  - **Random AI:** Simple random move selection for casual gameplay
  - **Q-Learning AI:** Advanced reinforcement learning agent that learns optimal strategies through self-play

## How to Play

### Interactive Mode

1. **Run the game:**
   ```bash
   python3 tictactoe.py
   ```

2. **Select game mode:**
   - Enter `0` for Computer vs Computer
   - Enter `1` for Human vs Computer
   - Enter `2` for Human vs Human

3. **Choose who starts (if playing against computer):**
   - Enter `H` for Human to start first (you play as X)
   - Enter `C` for Computer to start first (you play as O)

4. **Choose AI type (if playing against computer):**
   - Enter `R` for Random AI (simple, unpredictable moves)
   - Enter `L` for Q-Learning AI (trained, strategic play)

5. **Make your move:**
   - Enter a number from 1-9 to place your mark
   - The position reference shows which number corresponds to which cell:
     ```
     1 | 2 | 3
     ---------
     4 | 5 | 6
     ---------
     7 | 8 | 9
     ```

6. **Win the game:**
   - Get three in a row (horizontal, vertical, or diagonal) to win!
   - If all cells are filled with no winner, it's a draw

### Auto Mode (Automated Gameplay)

Run multiple games automatically without user interaction:

```bash
# Run 50 games (default)
python3 tictactoe.py -auto

# Run a custom number of games
python3 tictactoe.py -auto 100
```

**Features:**
- Computer vs Computer gameplay (no human players)
- Choose AI type at startup (Random, Q-Learning, or Deep Q-Learning)
- No user input required during gameplay
- Displays comprehensive statistics at the end:
  - Total games played
  - Number and percentage of wins for X
  - Number and percentage of wins for O
  - Number and percentage of draws

**Example output:**
```
==================================================
           TIC TAC TOE - AUTO MODE
==================================================

  Running 50 games (Computer vs Computer)...
  Please wait...

  Computer type: [R]andom or [L]earning (Q-Learning) or [D]eep Q-Learning? r
  Completed 10 / 50 games...
  Completed 20 / 50 games...
  Completed 30 / 50 games...
  Completed 40 / 50 games...
  Completed 50 / 50 games...

==================================================
                   RESULTS
==================================================

  Total games played: 50

  Player X wins:        33  ( 66.0%)
  Player O wins:        12  ( 24.0%)
  Draws:                 5  ( 10.0%)

==================================================
```

## Requirements

- Python 3.6 or higher
- No external dependencies required!

## Q-Learning Reinforcement Learning AI

This project includes an advanced AI player powered by **Q-Learning**, a fundamental reinforcement learning algorithm. This section explains how it works to help you learn about AI and machine learning.

### What is Q-Learning?

Q-Learning is a **model-free reinforcement learning algorithm** that learns to make optimal decisions by trial and error. The "Q" stands for "Quality" - the algorithm learns a quality value (Q-value) for each action in each state.

**Key Concepts:**

- **State (S):** The current configuration of the game board (e.g., "X O  X   " - a 9-character string)
- **Action (A):** A move the agent can make (placing a mark in positions 0-8)
- **Reward (R):** Feedback after an action (+1 for winning, -1 for losing, 0 for draw, -0.01 per move to encourage faster wins)
- **Q-Value Q(S,A):** The expected future reward for taking action A in state S
- **Policy:** The strategy the agent follows (choose the action with the highest Q-value)

### How Does It Learn?

The agent learns through **self-play** - it plays thousands of games against itself:

1. **Exploration vs Exploitation:** During training, the agent uses an ε-greedy strategy:
   - 90% of the time: Choose the action with the highest Q-value (exploitation)
   - 10% of the time: Choose a random action (exploration)

2. **Q-Value Updates:** After each move, the agent updates its Q-values using the formula:
   ```
   Q(s, a) ← Q(s, a) + α × [r + γ × max Q(s', a') - Q(s, a)]
   ```
   Where:
   - **α (alpha) = 0.2:** Learning rate (how much to update Q-values)
   - **γ (gamma) = 0.95:** Discount factor (how much to value future rewards)
   - **r:** Immediate reward
   - **s':** Next state
   - **max Q(s', a'):** Best possible future Q-value

3. **Reward Shaping:** The agent receives:
   - **+1** for winning a game
   - **-1** for losing a game
   - **0** for a draw
   - **-0.01** per move (small penalty to encourage faster wins)

4. **Temporal Difference Learning:** The agent updates Q-values incrementally during the game, not just at the end, allowing it to learn from partial game sequences.

### Training the AI

To train a new Q-Learning agent or improve the existing one:

```bash
python3 train_rl.py
```

This script:
- Creates a new RLAgent with default hyperparameters
- Trains it for 5,000 episodes of self-play
- Saves the learned Q-table to `q_table.json`

**Training Parameters:**
- **Episodes:** 5,000 games (takes about 30-60 seconds)
- **Alpha (learning rate):** 0.2
- **Gamma (discount factor):** 0.95
- **Epsilon (exploration rate):** 0.10

The Q-table stores thousands of state-action pairs and their Q-values. After training, the agent can play deterministically (no exploration) by always choosing the highest-valued action.

### Using the Trained AI

When you run the game and select the Q-Learning AI (option `L`), the program:

1. Loads the trained Q-table from `q_table.json`
2. For each move, converts the current board to a state string
3. Evaluates all legal moves and selects the one with the highest Q-value
4. Plays deterministically (no randomness), making it explainable and consistent

If `q_table.json` doesn't exist, the AI will still play but with untrained (zero-initialized) Q-values, resulting in random-like behavior.

### Why Q-Learning for Tic-Tac-Toe?

Tic-Tac-Toe is an excellent learning environment because:
- **Small state space:** The trained Q-table contains ~3,000-4,000 unique states and ~7,000 state-action pairs, making it manageable for storage and analysis
- **Clear rewards:** Win/lose/draw outcomes are unambiguous
- **Fast training:** Games are quick, allowing thousands of training episodes
- **Interpretable:** You can inspect the Q-table to understand what the agent learned
- **Perfect information:** No hidden state or randomness in game mechanics

This implementation demonstrates core RL concepts that scale to more complex problems like robotics, game AI, and decision-making systems.

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

## License

See LICENSE file for details.

