# train_rl.py  (top-level next to tictactoe.py, or inside the package if you prefer)
from tictactoe_package.rl_agent import RLAgent

if __name__ == "__main__":
    agent = RLAgent(alpha=0.2, gamma=0.95, epsilon=0.10)
    print("Training RL agent by self-play (5,000 episodes)…")
    agent.train_self_play(episodes=5000)
    agent.save("q_table.json")
    print("Saved learned policy to q_table.json")
