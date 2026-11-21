import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/comparison_results.csv")

metrics = [
    ("avg_vehicle_waiting_time", "Average Vehicle Waiting Time"),
    ("avg_stopped", "Average Stopped Vehicles"),
    ("avg_speed", "Average Speed"),
    ("total_reward", "Total Reward"),
]

controllers = ["Q-learning", "Fixed-time"]

for metric, title in metrics:
    means = df.groupby("controller")[metric].mean()
    stds = df.groupby("controller")[metric].std()

    means = means.reindex(controllers)
    stds = stds.reindex(controllers)

    plt.figure(figsize=(8, 5))
    plt.bar(
        controllers,
        means,
        yerr=stds,
        capsize=5,
    )

    plt.title(title)
    plt.ylabel(title)
    plt.tight_layout()

    filename = f"results/{metric}_comparison.png"
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"Saved {filename}")