# Smart Traffic Control System

## 1. Project Overview
 The Concept: Control the light phases (Green/Red timing) for a busy 4-way intersection based on live queue lengths in each lane.
 Why it’s manageable:
 You can use lightweight simulators like SUMO (Simulation of Urban MObility) or build a simple queuing system in Python.
 The goal is clear: maximize throughput and minimize vehicle delay.
 Baseline to beat: Fixed-timer traffic lights (e.g., green for 30 seconds every cycle).
Project Execution Blueprint: 
1. Use Gymnasium & Stable-Baselines3: Don't write every algorithm from scratch unless required. Use SB3's pre-implemented algorithms (PPO, DQN, A2C) to spend more time on environment tuning, reward shaping, and analysis.
2. Focus on Reward Shaping: For your report, a great section to write is comparing how different reward structures affect learning (e.g., penalizing time vs. penalizing collisions).
3. Clear Metrics: Measure success with concrete plots—Average Reward over Episodes, Time to Convergence, and Performance vs. Heuristic Baselines.

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

The current project directory is organized as follows:

```text
Smart-Traffic-Control-System/
│
├── sumo/
│   ├── intersection.net.xml
│   ├── routes.rou.xml
│   ├── simulation.sumocfg
│   ├── nodes.nod.xml
│   ├── edges.edg.xml
│   └── gui_settings.sumocfg
│
├── agent/
│   └── q_learning.py
│
├── controllers/
│   └── fixed_time.py
│
├── training/
│   └── train.py
│
├── evaluation/
│   ├── metrics.py
│   └── compare.py
│
├── results/
│
├── main.py
├── requirements.txt
└── README.md
```

PROPOSAL FEEDBACK:

Topic: Clear and reasonable. RL could help the agent adapt to changing traffic.

Method: The state, action, and reward design make sense. Also consider how you will simplify the states, since too many combinations could make tabular Q-learning difficult. Consider using DQN directly if needed.

Evaluation: Clear metrics and baselines, with tests under different traffic conditions.


### For Information regarding setup please refer to [INSTRUCTIONS.md](https://github.com/VaibhavSatish/Smart-Traffic-Control-System/blob/main/INSTRUCTIONS.md)
