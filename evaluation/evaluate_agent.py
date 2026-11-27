import json
from pathlib import Path
import sys

import gymnasium as gym
import sumo_rl
import pickle
import numpy as np

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from agent.q_learning import QLearningTrafficAgent, get_state
from agent.custom_reward import custom_reward
from evaluation.output_paths import create_run_directory


def evaluate(sumo_seed=42, output_dir=None):
    # Create the environment
    env = gym.make(
        "sumo-rl-v0",
        net_file=str(REPOSITORY_ROOT / "sumo/intersection.net.xml"),
        route_file=str(REPOSITORY_ROOT / "sumo/routes.rou.xml"),
        use_gui=False,
        num_seconds=600,
        sumo_seed=sumo_seed,
        reward_fn=custom_reward,
    )

    # Create the agent and load the trained Q-table
    agent = QLearningTrafficAgent()
    with open(REPOSITORY_ROOT / "results/q_table.pkl", "rb") as f:
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

    results = {
        "total_reward": sum(rewards),
        "avg_waiting_time": float(np.mean(waiting_times)),
        "avg_stopped": float(np.mean(stopped_counts)),
        "avg_speed": float(np.mean(speeds)),
        "avg_vehicle_waiting_time": float(np.mean(mean_waiting_times)),
    }

    print("\n========== EVALUATION RESULTS ==========")
    for metric, value in results.items():
        print(f"{metric}: {value:.3f}")

    if output_dir is None:
        output_dir = create_run_directory(f"q_learning_evaluation_seed_{sumo_seed}")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / f"q_learning_seed_{sumo_seed}.json"
    with result_path.open("w") as f:
        json.dump({"seed": sumo_seed, **results}, f, indent=2)
    print(f"Saved evaluation data to {result_path}")

    return results


if __name__ == "__main__":
    evaluate()
