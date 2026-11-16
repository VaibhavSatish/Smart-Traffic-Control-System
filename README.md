# Smart Traffic Control System

## 1. Project Overview
This project aims to develop an intelligent traffic signal control system that adapts to real-time traffic conditions at a busy four-way intersection. Rather than relying on fixed signal schedules, the system will dynamically adjust traffic light phases based on vehicle queue lengths and congestion across the intersection's incoming lanes.

The primary objective is to improve traffic flow by maximizing vehicle throughput while minimizing average vehicle waiting time and overall congestion. The system will learn to make traffic signal decisions that respond to changing traffic demand, allowing it to allocate green-light time where it is needed most.

To evaluate its effectiveness, the intelligent controller will be compared against a traditional fixed-time traffic signal system, which operates on a predetermined schedule regardless of current traffic conditions. This baseline will help determine whether adaptive control can produce measurable improvements in intersection performance.

The project will also explore how different reward structures influence the controller's learning and decision-making. By examining the effects of different approaches to rewarding efficient traffic flow and penalizing delays or undesirable outcomes, we aim to better understand how learning objectives affect overall performance.

Performance will be evaluated using metrics such as average vehicle waiting time, traffic throughput, congestion levels, and learning progress over time. Results will be presented through visualizations and comparisons with the fixed-time baseline to assess the effectiveness, consistency, and potential benefits of adaptive traffic signal control.

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
