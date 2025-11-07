# TicTacToe - 80's Edition

A console-based TicTacToe game inspired by Wargames and classic 80's computer games.

*"In the beginning, the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move. Shortly thereafter, someone invented TicTacToe, which was slightly less controversial but equally inevitable."* – Not Douglas Adams, but probably should have been.

## Features

Welcome, intrepid explorer, to a game so ancient that even your grandparents' Commodore 64 would find it quaint. Don't Panic! Despite its simplicity, this implementation packs more artificial intelligence than a depressed robot and more game modes than you can shake a towel at.

- **3 Game Modes:**
  - **Interactive Mode**: Human vs Human, Human vs Computer, or Computer vs Computer
  - **Auto Mode**: Computer vs Computer (for when you want to watch AI fight itself while you make tea)
  - **Training Mode**: Teach your AI to be less terrible at TicTacToe (spoiler: it works!)

- **Classic 80's Style:**
  - Fixed-width console display (because pixel-perfect graphics are overrated)
  - Retro ASCII graphics (we call it "vintage," you call it "my eyes hurt")
  - Simple and intuitive interface (even a Vogon could use it, though they wouldn't enjoy it)

- **Three AI Options:**
  - **Random AI:** About as strategic as flipping coins. Perfect for when you need a confidence boost.
  - **Q-Learning AI:** Learns from experience like a digital Arthur Dent stumbling through the universe.
  - **Deep Q-Learning AI:** Uses neural networks. Basically magic, but the kind that actually works.

## Game Modes Explained (Because Reading Instructions is Fundamental)

This TicTacToe implementation offers three distinct ways to play, each more entertaining than watching paint dry, though admittedly that's a low bar.

### Mode 1: Interactive Mode - *"The Social Experience"*

> *"I've seen it. It's rubbish."* – Marvin, probably about his opponents' strategies

This is your standard, run-of-the-mill, perfectly cromulent way to play TicTacToe. Humans and/or computers take turns, drama ensues, someone wins (or doesn't), and the universe continues its slow heat death.

**How to Use:**

1. **Launch the game:**
   ```bash
   python3 tictactoe.py
   ```

2. **Choose your adventure** - Number of human players:
   - Enter `0` for Computer vs Computer (spectator sport mode)
   - Enter `1` for Human vs Computer (the classic man-vs-machine showdown)
   - Enter `2` for Human vs Human (for when you have actual friends)

3. **Select AI difficulty** (if computers are playing):
   - Enter `R` for Random AI - Moves like a caffeinated squirrel. Zero strategy, maximum unpredictability.
   - Enter `L` for Q-Learning AI - Has learned from thousands of games. Still loses sometimes because TicTacToe is hard, okay?
   - Enter `D` for Deep Q-Learning AI - Uses neural networks and makes you feel like you're living in the future.

4. **Pick who goes first** (if playing against computer):
   - Enter `H` for Human first (you play as X, the traditional advantage)
   - Enter `C` for Computer first (computer plays as X, you play as O, prepare for suffering)

5. **Make your move:**
   - Enter a number from 1-9 corresponding to the board position:
     ```
     1 | 2 | 3
     ---------
     4 | 5 | 6
     ---------
     7 | 8 | 9
     ```
   - Try not to type random numbers. The game judges you silently.

6. **Win the game:**
   - Get three in a row (horizontal, vertical, or diagonal) to achieve victory!
   - Fill all cells with no winner to achieve a draw (the most common outcome when both players know what they're doing)

### Mode 2: Auto Mode - *"For Science!"*

> *"The Answer to the Great Question... of Life, the Universe and Everything... is... Forty-two."*  
> *"And what percentage of these 100 TicTacToe games ended in a draw?"*  
> *"...also Forty-two."*

Want to see computers battle it out while you grab a Pan Galactic Gargle Blaster? This mode runs multiple games automatically without requiring your meat-based input.

**How to Use:**

```bash
# Run 50 games (default)
python3 tictactoe.py -auto

# Run a custom number of games (because sometimes 42 is the right answer)
python3 tictactoe.py -auto 100
```

**What Happens:**
- Computer vs Computer gameplay exclusively (humans need not apply)
- Choose your AI type at startup (Random, Q-Learning, or Deep Q-Learning)
- The game runs faster than you can say "Don't Panic" 
- Comprehensive statistics appear at the end (spoiler: draws are common with competent AI)

**Statistical Output Includes:**
- Total games played (counting is important)
- Wins for X (with percentage, because raw numbers are so primitive)
- Wins for O (also with percentage)
- Draws (the sophisticated outcome for well-matched opponents)

**Example Output:**
```
==================================================
           TIC TAC TOE - AUTO MODE
==================================================

  Running 50 games (Computer vs Computer)...
  Please wait...

  Computer type: [R]andom or [L]earning (Q-Learning) or [D]eep Q-Learning? l
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

**Use Cases:**
- Testing AI performance (for science!)
- Generating training data (for more science!)
- Procrastinating productively (the best kind of procrastination)
- Proving that computers are better at TicTacToe than your cousin Gary

### Mode 3: Training Mode - *"Teaching Rocks to Think"*

> *"The usual procedure, of course, is to send a lightly armed battle cruiser to do battle with the Death Star's defenses, but I've managed to bypass that bit by teaching a neural network to play TicTacToe instead."*

Sometimes Random AI isn't random enough, and sometimes it's too random. The solution? Teach an AI to play properly through the ancient art of repeatedly making it play against itself until it achieves enlightenment (or at least competence).

**Training Q-Learning AI:**

```bash
python3 train_rl.py
```

This command will:
- Create a Q-Learning agent (like raising a digital puppy, but less messy)
- Make it play 5,000 games against itself (self-play, not self-harm)
- Save the learned wisdom to `q_table.json` (about 30-60 seconds of computation)
- Generate an AI that actually knows what it's doing

**Training Deep Q-Learning AI:**

```bash
python3 train_dqn.py
```

This command will:
- Create a Deep Q-Network agent (now with more layers!)
- Run 30,000 training episodes (neural networks are slower learners, like really smart but distractible students)
- Train against both itself AND a smart opponent (variety is the spice of learning)
- Save the neural network to `dqn_policy.pt`
- Take several minutes, so maybe put the kettle on

**What Gets Saved:**
- `q_table.json`: A lookup table of ~7,000 state-action pairs (Q-Learning's brain)
- `dqn_policy.pt`: Neural network weights (Deep Q-Learning's brain)

**When to Retrain:**
- When you're curious about machine learning
- When you want to experiment with different training parameters
- When you've broken the existing trained models
- When you're bored and have a few minutes to spare

## The AI Minds: Understanding Q-Learning and Deep Q-Learning

> *"The major difference between a thing that might go wrong and a thing that cannot possibly go wrong is that when a thing that cannot possibly go wrong goes wrong it usually turns out to be impossible to get at or repair."*
> 
> Fortunately, when AI goes wrong in TicTacToe, the worst outcome is losing to a 3x3 grid. Here's how we taught our silicon friends to play.

### Q-Learning: The Classic Approach

**What is Q-Learning, Really?**

Imagine you're Arthur Dent trying to navigate the complexities of the universe with nothing but a towel and a questionable guidebook. Q-Learning is basically that, but for games: the AI builds its own guidebook (called a Q-table) by playing thousands of games and remembering which moves led to victory and which led to existential despair.

**The "Q" stands for "Quality"** - each entry in the Q-table stores a quality score for taking a particular action in a particular state. Higher scores mean "probably a good idea," lower scores mean "you might as well concede now."

**Core Concepts (Without the Boring Bits):**

- **State (S):** The current board configuration, like "X O  X   " (a 9-character string representing the board)
- **Action (A):** A move you can make (placing your mark in positions 0-8)
- **Reward (R):** Feedback from the universe about your life choices:
  - **+1.0** for winning (sweet, sweet victory)
  - **-1.0** for losing (the agony of defeat)
  - **0** for a draw (the philosophical middle ground)
  - **-0.01** per move (encourages finishing quickly, like a cosmic parking meter)
- **Q-Value Q(S,A):** The expected future reward for taking action A in state S (fortune-telling, but with math)
- **Policy:** The strategy the agent follows (usually "pick the action with the highest Q-value" - groundbreaking stuff)

**How Does It Learn? (The Magic Revealed)**

The agent learns through **self-play** - it plays thousands of games against itself, like a lonely child with a mirror:

1. **Exploration vs Exploitation:** During training, the agent uses an ε-greedy strategy:
   - **90% of the time:** Choose the action with the highest Q-value (exploitation - "I know this works")
   - **10% of the time:** Choose a random action (exploration - "what if I try this crazy thing?")
   
   This balance prevents the AI from getting stuck in local optima, which is fancy talk for "doing the same mediocre thing forever."

2. **Q-Value Updates:** After each move, the agent updates its Q-values using the Bellman equation:
   ```
   Q(s, a) ← Q(s, a) + α × [r + γ × max Q(s', a') - Q(s, a)]
   ```
   
   Where (brace yourself for some math):
   - **α (alpha) = 0.2:** Learning rate (how much to update Q-values - too high and you're impulsive, too low and you're stubborn)
   - **γ (gamma) = 0.95:** Discount factor (how much to value future rewards - high values mean "plan ahead," low values mean "YOLO")
   - **r:** Immediate reward (what just happened)
   - **s':** Next state (where you ended up)
   - **max Q(s', a'):** Best possible future Q-value (optimism about the future)

3. **Reward Shaping:** The carrot-and-stick approach:
   - **+1** for winning (celebration time!)
   - **-1** for losing (sad trombone sound)
   - **0** for a draw (shrug emoji)
   - **-0.01** per move (small penalty to encourage efficiency - nobody likes a game that drags on)

4. **Temporal Difference Learning:** The agent doesn't wait until the game ends to learn. It updates Q-values after every single move, learning from partial game sequences. It's like learning from your mistakes in real-time rather than dwelling on them at 3 AM.

**Training the Q-Learning AI:**

To train a new Q-Learning agent or improve the existing one:

```bash
python3 train_rl.py
```

**What Happens During Training:**
- Creates a fresh RLAgent with default hyperparameters
- Plays 5,000 episodes of self-play (takes about 30-60 seconds)
- Saves the learned Q-table to `q_table.json`

**Training Parameters:**
- **Episodes:** 5,000 games (more would be better, but we're not trying to achieve AGI here)
- **Alpha (learning rate):** 0.2 (sweet spot between "slow learner" and "goldfish memory")
- **Gamma (discount factor):** 0.95 (values future rewards highly - this AI plans ahead)
- **Epsilon (exploration rate):** 0.10 (10% randomness keeps things interesting)

**The Q-Table:**

After training, the Q-table contains thousands of state-action pairs:
- **~3,000-4,000 unique states** (not all possible board configurations, just the ones that actually occur)
- **~7,000 state-action pairs** (state × valid actions for that state)
- Stored in human-readable JSON format (feel free to peek inside and see what the AI learned)

**Using the Trained Q-Learning AI:**

When you select the Q-Learning AI (option `L`) in the game:

1. Loads the trained Q-table from `q_table.json`
2. For each move, converts the current board to a state string
3. Evaluates all legal moves and selects the one with the highest Q-value
4. Plays deterministically (no randomness), making it consistent and predictable (unlike real humans)

If `q_table.json` doesn't exist, the AI will still play but with untrained (zero-initialized) Q-values, essentially becoming a very confused Random AI.

**Why Q-Learning for TicTacToe?**

TicTacToe is the goldfish of game AI - perfect for learning because:
- **Small state space:** Manageable number of board configurations (your laptop won't explode)
- **Clear rewards:** Win/lose/draw outcomes are unambiguous (unlike life)
- **Fast training:** Games are quick, allowing thousands of training episodes in under a minute
- **Interpretable:** You can inspect the Q-table and understand what the agent learned (transparency!)
- **Perfect information:** No hidden state or randomness in game mechanics (what you see is what you get)

This implementation demonstrates core reinforcement learning concepts that scale to more complex problems like robotics, game AI, autonomous driving, and teaching robots to fetch your slippers.

### Deep Q-Learning (DQN): The Neural Network Approach

**What is Deep Q-Learning?**

> *"Deep in the fundamental heart of mind and Universe there is a reason... Actually, probably not. But there IS a neural network, and it's trying its best."*

If Q-Learning is like having a guidebook, Deep Q-Learning is like having a guidebook written by a neural network that can generalize from examples. Instead of storing a massive table of every possible state, DQN uses a neural network to approximate the Q-function. It's like teaching someone to recognize patterns rather than memorizing every individual instance.

**Why Deep Q-Learning?**

Traditional Q-Learning works great for TicTacToe because the state space is small (~7,000 state-action pairs). But what if you wanted to play chess? Or Go? Or navigate a robot through a warehouse? Suddenly, you'd need to store gazillions of state-action pairs. That's where Deep Q-Learning comes in:

- **Function Approximation:** Instead of a lookup table, uses a neural network to estimate Q-values
- **Generalization:** Can handle states it has never seen before (like a student applying learned concepts to new problems)
- **Scalability:** Works for games and problems with massive state spaces
- **Modern Magic:** Uses the same technology that powers self-driving cars, game-playing AIs, and that thing that recommends what to watch next

**How Does DQN Work?**

DQN combines Q-Learning with neural networks, creating a beautiful marriage of classical and modern AI:

**1. Neural Network Architecture:**
```
Input Layer (28 neurons):
  - 27 neurons for board state (one-hot encoding: 3 values per cell × 9 cells)
  - 1 neuron for current player (+1 for X, -1 for O)

Hidden Layers:
  - 2 hidden layers with 64 neurons each
  - ReLU activation (because neurons should be excited about learning)

Output Layer (9 neurons):
  - One Q-value prediction for each possible position (1-9)
```

**2. Experience Replay:**
Unlike Q-Learning which learns from each experience immediately, DQN stores experiences in a "replay buffer" (up to 50,000 memories) and randomly samples batches for training. This is like studying from randomly shuffled flashcards instead of memorizing in sequence.

Why does this help?
- **Breaks correlation:** Consecutive game states are similar, which can make learning unstable
- **Efficient reuse:** Each experience can be learned from multiple times
- **Stable learning:** Random sampling smooths out the learning process

**3. Target Network:**
DQN uses TWO neural networks:
- **Q-Network (qnet):** The main network that we're actively training
- **Target Network (target):** A delayed copy that provides stable Q-value targets

The target network gets updated every 200 training steps, preventing the "chasing a moving target" problem. It's like having a study buddy who doesn't change their answers every five seconds.

**4. Training Against a Smart Opponent:**
Every 4th training episode, the DQN plays against a "smart opponent" that:
- Tries to win if it can
- Blocks the opponent's winning moves
- Takes the center if available
- Prefers corners over edges
- Falls back to random moves

This mixed training (75% self-play, 25% smart opponent) teaches the DQN both offensive and defensive strategies.

**5. The Critical Fix: Learning from Losses:**

Originally, the DQN had a major flaw: when a player made a move that led to their opponent winning on the next turn, that player's move was stored with just a small penalty (-0.01) and never learned it was actually terrible.

**The Fix:**
- Track the previous player's move
- When the current player wins, also store the previous player's move with a loss reward (-1.0)
- Now the AI learns "if I make this move, my opponent will win"

This simple fix improved the DQN's performance dramatically:
- **Before fix:** 64% losses, 36% draws when playing as X against smart opponent
- **After fix:** 33% losses, 67% draws when playing as X (86% improvement in draw rate!)

**Training the Deep Q-Learning AI:**

```bash
python3 train_dqn.py
```

**What Happens During Training:**
- Creates a DQN agent with a neural network
- Runs 30,000 training episodes (several minutes - time for tea!)
- Alternates between self-play and playing against a smart opponent
- Uses experience replay and target networks for stable learning
- Saves the trained network to `dqn_policy.pt`

**Training Parameters:**
- **Episodes:** 30,000 (neural networks need more examples than lookup tables)
- **Gamma (discount factor):** 0.99 (slightly higher than Q-Learning - planning further ahead)
- **Learning rate:** 0.001 (how fast the neural network updates)
- **Epsilon decay:** Starts at 1.0 (100% random), decays to 0.05 over 20,000 steps
- **Batch size:** 64 experiences per training update
- **Replay buffer:** 50,000 experiences (more memory than a goldfish, less than an elephant)

**Performance Characteristics:**

Against a smart opponent (100 games each):
- **As X (going first):** 33% losses, 67% draws, 0% wins
  - First move advantage helps significantly
  - Excellent defensive play prevents losses most of the time
  
- **As O (going second):** 100% losses, 0% draws, 0% wins
  - Going second in TicTacToe is brutal against optimal play
  - This is actually normal - even perfect play loses as O against perfect play as X

- **Against itself:** 100% draws
  - When both players are equally skilled and deterministic, draws are guaranteed
  - Perfectly balanced, as all things should be

**Using the Trained DQN AI:**

When you select the Deep Q-Learning AI (option `D`) in the game:

1. Loads the neural network from `dqn_policy.pt`
2. For each move, encodes the current board state
3. Feeds the state through the neural network
4. Gets Q-value predictions for all 9 positions
5. Masks out illegal moves
6. Selects the position with the highest Q-value
7. Can optionally explain its reasoning (verbose mode shows top candidates and their Q-values)

If `dqn_policy.pt` doesn't exist, you'll be politely informed and the game falls back to Random AI.

**Q-Learning vs Deep Q-Learning: The Showdown**

| Aspect | Q-Learning | Deep Q-Learning |
|--------|-----------|----------------|
| **Storage** | ~7,000 entries in JSON | Neural network weights |
| **Training Time** | 30-60 seconds | Several minutes |
| **Memory Usage** | Tiny (~300KB) | Small (~50KB) |
| **Generalization** | None (only knows trained states) | Can handle unseen states |
| **Complexity** | Simple, interpretable | Complex, black box-ish |
| **Scalability** | Poor for large state spaces | Excellent for large state spaces |
| **Performance** | Excellent for TicTacToe | Excellent for TicTacToe |
| **Best For** | Small, discrete problems | Large, complex problems |

For TicTacToe, both work excellently! Q-Learning is simpler and trains faster. Deep Q-Learning demonstrates modern techniques that scale to complex real-world problems like robotics, autonomous vehicles, and playing Starcraft.

**The Philosophical Question:**

Do we need neural networks for TicTacToe? Absolutely not. Should we use them anyway for educational purposes and because it's cool? *Absolutely yes.*

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

## Requirements

> *"Space," it says, "is big. Really big. You just won't believe how vastly, hugely, mindbogglingly big it is."*
> 
> Our requirements are the opposite of space. They're small. Really small.

**Core Requirements:**
- Python 3.10 or higher (because we're not savages)
- A terminal/console that supports basic ASCII (if you're reading this, you probably have one)

**For Basic Play (Human vs Human, Human vs Random AI):**
- No external dependencies! Zero. Zilch. Nada.
- Pure Python standard library
- Works on any system with Python

**For Q-Learning AI:**
- No additional dependencies required
- Uses JSON for storage (part of Python standard library)

**For Deep Q-Learning AI:**
- PyTorch 2.4.1 or higher (for neural network magic)
- NumPy 1.26.4 or higher (for number crunching)
- Optional: CUDA 12.3+ for GPU acceleration (but CPU works fine for TicTacToe)

**Installation:**

```bash
# Clone the repository
git clone https://github.com/dvroegop/tictactoe_python.git
cd tictactoe_python

# For basic play (no installation needed!)
python3 tictactoe.py

# For Deep Q-Learning support
pip install -r requirements.txt
```

**Platform Support:**
- Linux (the penguin approves)
- macOS (the apple is polished)
- Windows (the windows are... functional)
- Anything that runs Python 3.10+ (including your toaster, if you're brave enough)

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

## Frequently Asked Questions (That Nobody Asked But We're Answering Anyway)

**Q: Which AI should I play against?**  
A: 
- Random AI: If you need a confidence boost or just want chaos
- Q-Learning AI: If you want a respectable challenge  
- Deep Q-Learning AI: If you want to see neural networks in action

**Q: Why does the AI sometimes lose to obviously bad moves?**  
A: Even trained AIs aren't perfect. TicTacToe has optimal strategies, but achieving perfect play requires exploring all ~255,168 possible games. Our AIs are very good, not omniscient.

**Q: Can I beat the trained AIs?**  
A: Yes! Especially if you're paying attention. The AIs play well but aren't unbeatable. Going first (as X) gives you a significant advantage.

**Q: How long does training take?**  
A: 
- Q-Learning: 30-60 seconds (grab a snack)
- Deep Q-Learning: Several minutes (make tea, contemplate existence)

**Q: Can I modify the training parameters?**  
A: Absolutely! Edit `train_rl.py` or `train_dqn.py` and experiment. Science is all about trial and error (mostly error).

**Q: Will this teach me machine learning?**  
A: Yes! This is a great introduction to:
- Reinforcement Learning fundamentals
- Q-Learning and temporal difference learning
- Deep Q-Networks and neural networks
- Experience replay and target networks
- Reward shaping and exploration vs exploitation

**Q: Why TicTacToe? It's so simple!**  
A: Exactly! It's simple enough to understand completely but complex enough to demonstrate real AI concepts. It's the "Hello World" of reinforcement learning.

**Q: Where are all the Douglas Adams references?**  
A: *waves hands* They're everywhere! Don't Panic if you missed them.

## Troubleshooting

**"ModuleNotFoundError: No module named 'torch'"**
- You tried to use Deep Q-Learning without installing PyTorch
- Solution: `pip install -r requirements.txt` or just use Q-Learning instead

**"No q_table.json found; the AI will still play, but may be weak."**
- The Q-Learning AI hasn't been trained yet
- Solution: Run `python3 train_rl.py` to train it

**"No DQN policy loaded; using random fallback."**
- The Deep Q-Learning AI hasn't been trained yet  
- Solution: Run `python3 train_dqn.py` to train it (grab a beverage, this takes a few minutes)

**The AI keeps losing!**
- Did you train it? Untrained AIs are essentially random
- Training files needed: `q_table.json` for Q-Learning, `dqn_policy.pt` for Deep Q-Learning

**The game is too easy/hard!**
- Easy: Play against Random AI
- Medium: Play against Q-Learning AI
- Hard: Play against Deep Q-Learning AI
- Impossible: Play optimally against a perfectly trained AI while going second

## Contributing

Found a bug? Have an idea? Want to add a new AI algorithm?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (we have tests! Use them!)
5. Submit a pull request
6. Wait patiently while maintaining a positive attitude and possibly towel

## Educational Value

This project demonstrates:
- **Game Theory:** Understanding optimal strategies in zero-sum games
- **Reinforcement Learning:** Learning from rewards and punishments
- **Q-Learning:** Value-based methods for decision making
- **Deep Learning:** Neural networks for function approximation
- **Software Engineering:** Clean code structure, testing, documentation
- **Console Applications:** Building interactive terminal programs
- **Python Programming:** Modern Python practices and patterns

Perfect for:
- Students learning AI and machine learning
- Developers exploring reinforcement learning
- Anyone curious about how game AI works
- People who really, really like TicTacToe

## License

See LICENSE file for details.

---

*"For a moment, nothing happened. Then, after a second or so, nothing continued to happen."* – Except this time something did happen: you learned about TicTacToe AI. Congratulations! 🎉

**Now go forth and play!** Remember to bring your towel.

