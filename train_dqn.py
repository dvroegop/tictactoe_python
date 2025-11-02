# train_dqn.py
from tictactoe_package.dqn_agent import DQNAgent, DQNConfig, encode_board, legal_mask
from tictactoe_package.game import TicTacToe  # your existing environment
import random

# ----- Constants -----

SMART_OPPONENT_FREQUENCY = 4  # Train against smart opponent every Nth episode

# ----- Helper Functions -----

def outcome_reward(winner: str | None, mover: str) -> float:
    if winner is None:
        return 0.0
    return +1.0 if mover == winner else -1.0

def check_winning_move(board, player):
    """Check if there's a winning move for the player.
    
    Returns position index if winning move exists, None otherwise.
    """
    # Winning combinations to check
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combo in winning_combinations:
        positions = [board[i] for i in combo]
        # Check if two positions have player's mark and one is empty
        if positions.count(player) == 2 and positions.count(' ') == 1:
            # Return the empty position that would complete the line
            empty_idx = positions.index(' ')
            return combo[empty_idx]
    
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

def train(episodes=30000):
    cfg = DQNConfig()
    cfg.verbose = False  # Disable verbose output during training for speed
    agent = DQNAgent(cfg)
    print(f"Device: {agent.cfg.device}")

    for ep in range(1, episodes + 1):
        env = TicTacToe()
        step_in_ep = 0
        # Track previous DQN player's experience to update when opponent wins
        prev_dqn_experience = None  # (state, action, mover)
        
        # Decide if this episode uses smart opponent (every Nth episode)
        use_smart = (ep % SMART_OPPONENT_FREQUENCY == 0)
        
        # In smart episodes, randomly decide if DQN plays X or O
        # dqn_player will be 'X' or 'O', and smart opponent plays the other
        if use_smart:
            dqn_player = random.choice(['X', 'O'])
        else:
            dqn_player = None  # DQN plays both sides
        
        # play one episode
        while True:
            s = encode_board(env.board, env.current_player)
            
            # Determine if this is a DQN move or smart opponent move
            is_smart_opponent_turn = use_smart and (env.current_player != dqn_player)
            
            if is_smart_opponent_turn:
                # Smart opponent's turn
                a = smart_opponent_move(env.board, env.current_player)
                if a is None:
                    break  # no legal moves
            else:
                # DQN's turn
                a = agent.select_action(env.board, env.current_player, explore=True)
                if a == -1:
                    break  # no legal moves

            # take action
            mover = env.current_player
            is_dqn_move = not is_smart_opponent_turn
            env.make_move(a)
            winner = env.check_winner()
            done = winner is not None or env.is_board_full()
            step_penalty = -0.01

            if done:
                r = outcome_reward(winner, mover) + step_penalty
                s_next = encode_board(env.board, env.current_player)  # terminal snapshot
                mask_next = legal_mask(env.board)
                
                # Only remember if this was a DQN move
                if is_dqn_move:
                    agent.remember(s, a, r, s_next, True, mask_next)
                    agent.step_count += 1
                    agent.learn()
                
                # If there was a previous DQN player and current player won, 
                # update previous DQN player's experience with negative reward
                if prev_dqn_experience is not None and winner is not None:
                    prev_s, prev_a, prev_mover = prev_dqn_experience
                    if winner != prev_mover:
                        # Previous DQN player's move led to opponent winning
                        prev_r = -1.0 + step_penalty  # Loss reward
                        prev_s_next = encode_board(env.board, prev_mover)  # terminal state from prev player's perspective
                        prev_mask_next = legal_mask(env.board)
                        agent.remember(prev_s, prev_a, prev_r, prev_s_next, True, prev_mask_next)
                        agent.step_count += 1
                        agent.learn()
                
                break
            else:
                # switch player and continue
                env.switch_player()
                r = step_penalty
                s_next = encode_board(env.board, env.current_player)
                mask_next = legal_mask(env.board)
                
                # Only remember if this was a DQN move
                if is_dqn_move:
                    agent.remember(s, a, r, s_next, False, mask_next)
                    agent.step_count += 1
                    agent.learn()
                    
                    # Store current experience as previous for next iteration
                    prev_dqn_experience = (s, a, mover)

            step_in_ep += 1

        if ep % 500 == 0:
            print(f"Episode {ep}/{episodes} | Buffer: {len(agent.buffer)} | Epsilon: {agent.epsilon():.2f}")

    agent.save("dqn_policy.pt")
    print("Saved DQN policy -> dqn_policy.pt")

if __name__ == "__main__":
    train(episodes=60000)
