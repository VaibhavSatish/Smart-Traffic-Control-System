import json
from pathlib import Path
import sys

import gymnasium as gym
import sumo_rl

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from evaluation.output_paths import create_run_directory


def run_diagnostics():
    output_dir = create_run_directory("environment_diagnostics")
    env = gym.make(
        "sumo-rl-v0",
        net_file=str(REPOSITORY_ROOT / "sumo/intersection.net.xml"),
        route_file=str(REPOSITORY_ROOT / "sumo/routes.rou.xml"),
        use_gui=False,
        num_seconds=600,
    )

    observation, info = env.reset()
    print("Initial info keys:", info.keys())
    diagnostic_steps = []

    for step in range(10):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        step_data = {"step": step + 1, "reward": reward, "info": info}
        diagnostic_steps.append(step_data)

        print(f"\nStep {step + 1}")
        print("Reward:", reward)
        print("Info:", info)

        if terminated or truncated:
            break

    env.close()
    diagnostic_path = output_dir / "environment_metrics.json"
    with diagnostic_path.open("w") as f:
        json.dump({"initial_info": info, "steps": diagnostic_steps}, f, indent=2, default=str)
    print(f"Saved diagnostic data to {diagnostic_path}")


if __name__ == "__main__":
    run_diagnostics()
