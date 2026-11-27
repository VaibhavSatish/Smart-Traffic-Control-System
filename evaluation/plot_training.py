from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from evaluation.output_paths import create_run_directory


def plot_training_rewards():
    # Training artifacts are still produced by training/train.py in results/.
    training_data = REPOSITORY_ROOT / "results/training_rewards.csv"
    data = pd.read_csv(training_data)
    rewards = data["total_reward"]
    rolling_average = rewards.rolling(window=5).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(data["episode"], rewards, label="Episode Reward", alpha=0.5)
    plt.plot(
        data["episode"],
        rolling_average,
        label="5-Episode Moving Average",
        linewidth=2,
    )
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Q-Learning Training Progress")
    plt.legend()
    plt.grid(True)

    output_dir = create_run_directory("training_plots")
    output_path = output_dir / "training_curve.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved {output_path}")


if __name__ == "__main__":
    plot_training_rewards()
