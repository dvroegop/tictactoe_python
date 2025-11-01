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
                break
            else:
                # switch player and continue
                env.switch_player()
                r = step_penalty
                s_next = encode_board(env.board, env.current_player)
                agent.remember(s, a, r, s_next, False)
                agent.step_count += 1
                agent.learn()

            step_in_ep += 1

        if ep % 500 == 0:
            print(f"Episode {ep}/{episodes} | Buffer: {len(agent.buffer)} | Epsilon: {agent.epsilon():.2f}")

    agent.save("dqn_policy.pt")
    print("Saved DQN policy -> dqn_policy.pt")

if __name__ == "__main__":
    train(episodes=8000)
