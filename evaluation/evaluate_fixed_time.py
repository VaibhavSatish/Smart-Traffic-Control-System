
import gymnasium as gym
import sumo_rl
import numpy as np

from controllers.fixed_time import fixed_time_action


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

    observation, info = env.reset()

    done = False
    step = 0

    # Collect metrics
    waiting_times = []
    mean_waiting_times = []
    stopped_counts = []
    speeds = []
    rewards = []

    while not done:

        # Choose action from fixed-time schedule
        action = fixed_time_action(step)

        observation, reward, terminated, truncated, info = env.step(action)

        done = terminated or truncated

        rewards.append(reward)

        waiting_times.append(info["system_total_waiting_time"])
        mean_waiting_times.append(info["system_mean_waiting_time"])
        stopped_counts.append(info["system_total_stopped"])
        speeds.append(info["system_mean_speed"])

        step += 1

    env.close()

    # Calculate evaluation metrics
    results = {
        "total_reward": sum(rewards),
        "avg_total_waiting_time": np.mean(waiting_times),
        "avg_vehicle_waiting_time": np.mean(mean_waiting_times),
        "avg_stopped": np.mean(stopped_counts),
        "avg_speed": np.mean(speeds),
    }

    print("\n========== FIXED-TIME EVALUATION ==========")

    for metric, value in results.items():
        print(f"{metric}: {value:.3f}")

    return results


if __name__ == "__main__":
    evaluate()
