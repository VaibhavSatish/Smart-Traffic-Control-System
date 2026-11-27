import csv
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from evaluation.evaluate_agent import evaluate as evaluate_q_learning
from evaluation.evaluate_fixed_time import evaluate as evaluate_fixed_time
from evaluation.output_paths import create_run_directory


SEEDS = [42, 43, 44, 45, 46]


def run_comparison():
    output_dir = create_run_directory("controller_comparison")
    all_results = []

    for seed in SEEDS:
        print(f"\n{'=' * 50}")
        print(f"RUNNING SEED {seed}")
        print(f"{'=' * 50}")

        q_results = evaluate_q_learning(sumo_seed=seed, output_dir=output_dir)
        fixed_results = evaluate_fixed_time(sumo_seed=seed, output_dir=output_dir)

        all_results.append({"seed": seed, "controller": "Q-learning", **q_results})
        all_results.append({"seed": seed, "controller": "Fixed-time", **fixed_results})

    filename = output_dir / "comparison_results.csv"
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

    with filename.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nAll results saved to {filename}")
    return output_dir


if __name__ == "__main__":
    run_comparison()
