import csv

from evaluate_agent import evaluate as evaluate_q_learning
from evaluate_fixed_time import evaluate as evaluate_fixed_time


SEEDS = [42, 43, 44, 45, 46]


def run_comparison():
    all_results = []

    for seed in SEEDS:
        print(f"\n{'=' * 50}")
        print(f"RUNNING SEED {seed}")
        print(f"{'=' * 50}")

        q_results = evaluate_q_learning(sumo_seed=seed)
        fixed_results = evaluate_fixed_time(sumo_seed=seed)

        all_results.append({
            "seed": seed,
            "controller": "Q-learning",
            **q_results,
        })

        all_results.append({
            "seed": seed,
            "controller": "Fixed-time",
            **fixed_results,
        })

    # Save results to CSV
    filename = "results/comparison_results.csv"
    fieldnames = [
    "seed",
    "controller",
    "total_reward",
    "avg_waiting_time",
    "avg_total_waiting_time",
    "avg_vehicle_waiting_time",
    "avg_stopped",
    "avg_speed",
]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nAll results saved to {filename}")


if __name__ == "__main__":
    run_comparison()