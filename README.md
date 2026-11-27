# Smart Traffic Control System

## Project overview

This project uses SUMO-RL and a custom Q-learning agent to control traffic signals at a four-way intersection. The agent observes current traffic conditions and selects signal actions, with the goal of improving traffic flow and reducing vehicle waiting time and congestion. Its performance can be compared with a fixed-time signal controller that follows a predetermined schedule.

Training uses a custom reward function and runs for 50 episodes. Evaluation records traffic and reward metrics, including average vehicle waiting time, stopped vehicles, speed, and total reward. Evaluation and training artifacts are saved in uniquely named, timestamped directories under `results/`, so a new run does not overwrite previous outputs.

### Technologies

| Technology | Purpose |
|---|---|
| Python 3.14 | Main programming language |
| SUMO 1.28.0 | Traffic simulation |
| SUMO-GUI | Graphical traffic visualization |
| SUMO-RL | Reinforcement-learning interface |
| Gymnasium | RL environment API |
| XQuartz | X11 display server for macOS |

## Project structure

```text
Smart-Traffic-Control-System/
├── agent/
│   ├── q_learning.py             # Q-learning agent and state discretization
│   └── custom_reward.py          # Reward function for traffic control
├── controllers/
│   └── fixed_time.py             # Fixed-time baseline controller
├── evaluation/
│   ├── evaluate_agent.py         # Evaluates the trained Q-learning agent
│   ├── evaluate_fixed_time.py    # Evaluates the fixed-time baseline
│   ├── run_comparison.py         # Compares both controllers across seeds 42–46
│   ├── metrics.py                # Inspects SUMO-RL rewards and environment info
│   ├── output_paths.py           # Creates timestamped output directories
│   ├── plot_comparison.py        # Plots controller comparison results
│   └── plot_training.py          # Plots training rewards
├── inspection_files/             # Environment and agent inspection scripts
├── sumo/                          # SUMO network, routes, and simulation config
├── training/
│   └── train.py                  # Trains the Q-learning agent for 50 episodes
├── results/                       # Generated runs and their artifacts
├── INSTRUCTIONS.md                # SUMO, SUMO-RL, and macOS setup instructions
├── requirements.txt               # Python dependencies
└── README.md
```

## Setup

Install and configure SUMO and SUMO-RL, then install the Python dependencies:

```bash
pip install -r requirements.txt
```

For detailed SUMO, SUMO-RL, and macOS setup instructions, see [INSTRUCTIONS.md](INSTRUCTIONS.md).

Run the following commands from the repository root.

## Train the agent

```bash
python training/train.py
```

Training runs 50 episodes and creates a directory like:

```text
results/q_learning_training_<timestamp>/
├── q_table.pkl
└── training_rewards.csv
```

The script prints the actual output directory when training completes.

## Evaluate and compare controllers

The evaluation scripts save per-seed metrics as JSON files in timestamped directories. Run the Q-learning and fixed-time evaluations individually with:

```bash
python evaluation/evaluate_agent.py
python evaluation/evaluate_fixed_time.py
```

`evaluate_agent.py` currently loads its Q-table from `results/q_table.pkl`. Training now saves the table in a timestamped training directory, so before running evaluation, copy the desired table to that expected path. For example, replace `<timestamp>` with the directory name printed by training:

```bash
cp results/q_learning_training_<timestamp>/q_table.pkl results/q_table.pkl
```

To compare both controllers over seeds 42–46, run:

```bash
python evaluation/run_comparison.py
```

This creates a directory like `results/controller_comparison_<timestamp>/` containing `comparison_results.csv` and JSON metric files for each controller and seed. The comparison also uses the Q-table at `results/q_table.pkl`, so copy the trained table there first.

## Plot results

To create comparison charts, run:

```bash
python evaluation/plot_comparison.py
```

The script reads the most recently modified `comparison_results.csv` in a `controller_comparison_*` directory and saves charts in a new `results/comparison_plots_<timestamp>/` directory.

To create a training-reward chart, `plot_training.py` currently reads `results/training_rewards.csv`. Copy the CSV from the selected timestamped training run to that path, then run:

```bash
cp results/q_learning_training_<timestamp>/training_rewards.csv results/training_rewards.csv
python evaluation/plot_training.py
```

The chart is saved in a new `results/training_plots_<timestamp>/` directory.

## Inspect the environment

```bash
python inspection_files/inspect_env.py
```
