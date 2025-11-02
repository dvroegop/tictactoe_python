# train_dqn.py
from tictactoe_package.dqn_agent import DQNAgent, DQNConfig, encode_board
from tictactoe_package.game import TicTacToe  # your existing environment

def outcome_reward(winner: str | None, mover: str) -> float:
    if winner is None:
        return 0.0
    return +1.0 if mover == winner else -1.0

def train(episodes=8000):
    agent = DQNAgent(DQNConfig())
    print(f"Device: {agent.cfg.device}")

    for ep in range(1, episodes + 1):
        env = TicTacToe()
        step_in_ep = 0
        # Track previous player's experience to update when opponent wins
        prev_experience = None  # (state, action, mover)
        
        # play one episode
        while True:
            s = encode_board(env.board, env.current_player)
            a = agent.select_action(env.board, env.current_player, explore=True)
            if a == -1:
                break  # no legal moves

            # take action
            mover = env.current_player
            env.make_move(a)
            winner = env.check_winner()
            done = winner is not None or env.is_board_full()
            step_penalty = -0.01

            if done:
                r = outcome_reward(winner, mover) + step_penalty
                s_next = encode_board(env.board, env.current_player)  # terminal snapshot (unused)
                agent.remember(s, a, r, s_next, True)
                agent.step_count += 1
                agent.learn()
                
                # If there was a previous player and current player won, 
                # update previous player's experience with negative reward
                if prev_experience is not None and winner is not None:
                    prev_s, prev_a, prev_mover = prev_experience
                    if winner != prev_mover:
                        # Previous player's move led to opponent winning
                        prev_r = -1.0 + step_penalty  # Loss reward
                        prev_s_next = encode_board(env.board, prev_mover)  # terminal state from prev player's perspective
                        agent.remember(prev_s, prev_a, prev_r, prev_s_next, True)
                        agent.step_count += 1
                        agent.learn()
                
                break
            else:
                # switch player and continue
                env.switch_player()
                r = step_penalty
                s_next = encode_board(env.board, env.current_player)
                agent.remember(s, a, r, s_next, False)
                agent.step_count += 1
                agent.learn()
                
                # Store current experience as previous for next iteration
                prev_experience = (s, a, mover)

            step_in_ep += 1

        if ep % 500 == 0:
            print(f"Episode {ep}/{episodes} | Buffer: {len(agent.buffer)} | Epsilon: {agent.epsilon():.2f}")

    agent.save("dqn_policy.pt")
    print("Saved DQN policy -> dqn_policy.pt")

if __name__ == "__main__":
    train(episodes=8000)
