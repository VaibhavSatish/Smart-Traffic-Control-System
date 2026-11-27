# Smart Traffic Control System

## 1. Project Overview

This project develops an intelligent traffic-signal controller for a busy four-way intersection using SUMO-RL and a custom Q-learning agent. It replaces fixed signal schedules with an agent that observes the traffic environment and dynamically decides whether to continue the current green phase or switch to the opposing green phase.

The primary objective is to improve traffic flow by maximizing vehicle throughput while minimizing average vehicle waiting time and overall congestion. The agent learns from vehicle queues and its current traffic-light phase, using the custom reward function to balance these competing goals.

The intelligent controller is evaluated against a traditional fixed-time traffic-signal system that alternates phases on a predetermined schedule regardless of current traffic conditions.

The project explores how different reward structures influence the controller's learning and decision-making. The custom reward penalizes accumulated waiting time and queued vehicles, rewards newly passing vehicles in the outgoing lanes, and discourages unnecessary signal switches.

Performance is evaluated using average vehicle waiting time, traffic throughput, congestion levels, and learning progress across episodes. The repository provides CSV exports and plots that compare the trained Q-learning agent with the fixed-time baseline.

### Technologies

| Technology | Purpose |
|---|---|
| Python 3.14 | Main programming language |
| SUMO 1.28.0 | Traffic simulation |
| SUMO-GUI | Graphical traffic visualization |
| SUMO-RL | Reinforcement learning interface |
| Gymnasium | RL environment API |
| XQuartz | X11 display server for macOS |

---

## 2. Project Structure

The repository is organized as follows:

```text
Smart-Traffic-Control-System/
├── agent/
│   ├── q_learning.py             # Q-learning agent and state discretization
│   └── custom_reward.py          # Custom reward combining waiting, queues, throughput, and switching
├── controllers/
│   └── fixed_time.py             # Fixed-time controller used as a baseline
├── evaluation/
│   ├── evaluate_agent.py         # Evaluates the trained Q-learning agent
│   ├── evaluate_fixed_time.py    # Evaluates the fixed-time baseline
│   ├── run_comparison.py         # Runs both controllers across multiple seeds
│   ├── metrics.py                # Inspects SUMO-RL reward and environment info
│   ├── plot_comparison.py        # Creates comparison charts from CSV results
│   └── plot_training.py          # Creates the training progress chart
├── inspection_files/
│   ├── inspect_env.py            # Inspects observations, lanes, and actions
│   ├── test_agent.py             # Tests the agent against the environment
│   ├── test_reward.py            # Tests the custom reward function
│   └── test_throughput.py        # Tests vehicle throughput tracking
├── sumo/
│   ├── nodes.nod.xml             # SUMO network nodes
│   ├── edges.edg.xml             # SUMO network edges
│   ├── intersection.net.xml      # Generated traffic network
│   ├── routes.rou.xml            # Routes and vehicle flows
│   ├── simulation.sumocfg        # SUMO simulation configuration
│   └── gui_settings.xml          # Saved SUMO-GUI visualization settings
├── training/
│   └── train.py                  # Trains the Q-learning agent for 50 episodes
├── results/
│   ├── q_table.pkl               # Saved trained Q-table
│   ├── training_rewards.csv      # Reward recorded during training
│   ├── training_curve.png        # Training progress visualization
│   ├── comparison_results.csv    # Q-learning versus fixed-time results
│   └── *_comparison.png          # Performance comparison charts
├── INSTRUCTIONS.md               # SUMO, SUMO-RL, and macOS setup instructions
├── requirements.txt              # Python dependencies
└── README.md
```

### Important files to run the project

Run commands from the repository root.

1. **Set up Python dependencies:** `requirements.txt`
2. **Configure the SUMO network:** `sumo/nodes.nod.xml`, `sumo/edges.edg.xml`, `sumo/routes.rou.xml`, and `sumo/simulation.sumocfg`
3. **Train the agent:** `training/train.py`
   ```bash
   python training/train.py
   ```
   This creates `results/q_table.pkl` and `results/training_rewards.csv`.
4. **Run the controller comparison:** `evaluation/run_comparison.py`
   ```bash
   python evaluation/run_comparison.py
   ```
   This loads the trained Q-table and compares it with `controllers/fixed_time.py`; it writes `results/comparison_results.csv`.
5. **Plot results:**
   ```bash
   python evaluation/plot_training.py
   python evaluation/plot_comparison.py
   ```
6. **Inspect or smoke-test the environment:** `inspection_files/inspect_env.py`
   ```bash
   python inspection_files/inspect_env.py
   ```

For detailed SUMO and SUMO-RL installation and configuration instructions, see [INSTRUCTIONS.md](INSTRUCTIONS.md).
