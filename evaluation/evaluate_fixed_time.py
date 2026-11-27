import json
from pathlib import Path
import sys

import gymnasium as gym
import sumo_rl
import numpy as np

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from controllers.fixed_time import fixed_time_action
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

    results = {
        "total_reward": sum(rewards),
        "avg_total_waiting_time": float(np.mean(waiting_times)),
        "avg_vehicle_waiting_time": float(np.mean(mean_waiting_times)),
        "avg_stopped": float(np.mean(stopped_counts)),
        "avg_speed": float(np.mean(speeds)),
    }

    print("\n========== FIXED-TIME EVALUATION ==========")
    for metric, value in results.items():
        print(f"{metric}: {value:.3f}")

    if output_dir is None:
        output_dir = create_run_directory(f"fixed_time_evaluation_seed_{sumo_seed}")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / f"fixed_time_seed_{sumo_seed}.json"
    with result_path.open("w") as f:
        json.dump({"seed": sumo_seed, **results}, f, indent=2)
    print(f"Saved evaluation data to {result_path}")

    return results


if __name__ == "__main__":
    evaluate()
