
import gymnasium as gym
import sumo_rl
import pickle
import numpy as np

from agent.q_learning import QLearningTrafficAgent, get_state


def evaluate(sumo_seed=42):

    # Create the environment
    env = gym.make(
        "sumo-rl-v0",
        net_file="sumo/intersection.net.xml",
        route_file="sumo/routes.rou.xml",
        use_gui=False,
        num_seconds=600,
        sumo_seed = sumo_seed, 
    )

    # Create the agent
    agent = QLearningTrafficAgent()

    # Load the trained Q-table
    with open("results/q_table.pkl", "rb") as f:
        agent.q_table.update(pickle.load(f))

    # Disable exploration
    agent.epsilon = 0

    observation, info = env.reset()

    done = False

    # Collect metrics at each environment step
    waiting_times = []
    mean_waiting_times = []
    stopped_counts = []
    speeds = []
    rewards = []

    while not done:

        state = get_state(observation)

        action = agent.choose_action(state)

        observation, reward, terminated, truncated, info = env.step(action)

        done = terminated or truncated

        rewards.append(reward)

        waiting_times.append(info["system_total_waiting_time"])
        stopped_counts.append(info["system_total_stopped"])
        speeds.append(info["system_mean_speed"])
        mean_waiting_times.append(info["system_mean_waiting_time"])

    env.close()

    # Calculate averages across simulation steps
    results = {
        "total_reward": sum(rewards),
        "avg_waiting_time": np.mean(waiting_times),
        "avg_stopped": np.mean(stopped_counts),
        "avg_speed": np.mean(speeds),
        "avg_vehicle_waiting_time": np.mean(mean_waiting_times),
    }

    print("\n========== EVALUATION RESULTS ==========")

    for metric, value in results.items():
        print(f"{metric}: {value:.3f}")

    return results


if __name__ == "__main__":
    evaluate()
