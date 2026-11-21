import gymnasium as gym
import sumo_rl
from agent.q_learning import QLearningTrafficAgent, get_state
import os
import pickle
import csv

def train():
    env = gym.make(
        "sumo-rl-v0",
        net_file="sumo/intersection.net.xml",
        route_file="sumo/routes.rou.xml",
        use_gui=False,
        num_seconds=600,
    )
    agent = QLearningTrafficAgent()
    num_episodes = 50
    episode_rewards = []
    for episode in range(num_episodes):
        observation, info = env.reset()
        state = get_state(observation)
        total_reward = 0
        done = False
        while not done:
            action = agent.choose_action(state)
            next_observation, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            next_state = get_state(next_observation)
            agent.learn(state, action, reward, next_state, done)
            total_reward += reward
            state = next_state
        agent.decay_exploration()
        episode_rewards.append(total_reward)
        print(
            f"Episode {episode + 1}/{num_episodes} | "
            f"Total Reward: {total_reward:.2f} | "
            f"Epsilon: {agent.epsilon:.3f}"
        )
    os.makedirs("results", exist_ok=True)
    with open("results/q_table.pkl", "wb") as f:
        pickle.dump(dict(agent.q_table), f)
    with open("results/training_rewards.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["episode", "total_reward"])

        for i, reward in enumerate(episode_rewards):
            writer.writerow([i + 1, reward])
    env.close()
    return agent

if __name__ == "__main__":
    train()

