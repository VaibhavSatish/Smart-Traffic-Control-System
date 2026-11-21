
import pandas as pd
import matplotlib.pyplot as plt


def plot_training_rewards():

    # Load training rewards
    data = pd.read_csv("results/training_rewards.csv")

    rewards = data["total_reward"]

    # Calculate a rolling average to smooth the curve
    rolling_average = rewards.rolling(window=5).mean()

    # Plot
    plt.figure(figsize=(10, 5))

    plt.plot(
        data["episode"],
        rewards,
        label="Episode Reward",
        alpha=0.5
    )

    plt.plot(
        data["episode"],
        rolling_average,
        label="5-Episode Moving Average",
        linewidth=2
    )

    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Q-Learning Training Progress")

    plt.legend()
    plt.grid(True)

    # Save the figure
    plt.savefig("results/training_curve.png", dpi=300)

    plt.show()


if __name__ == "__main__":
    plot_training_rewards()
