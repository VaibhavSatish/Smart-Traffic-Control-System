
## 3. SUMO Installation and Configuration

SUMO was installed on macOS and its executable was verified.

Check the installation:

```bash
which sumo
```

On the working development machine, the output was:

```text
/opt/homebrew/bin/sumo
```

Check the installed version:

```bash
sumo --version
```

The installed version is SUMO 1.28.0.

### SUMO_HOME configuration

The SUMO tools directory was located at:

```text
/opt/homebrew/lib/python3.14/site-packages/sumo
```

The following environment variables were configured:

```bash
export SUMO_HOME="/opt/homebrew/lib/python3.14/site-packages/sumo"
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
```

These variables allow Python to locate SUMO's tools and libraries.

**Important:** Installation paths can differ between group members. Each person should verify their own SUMO installation before copying these paths.

---

## 4. Creating the SUMO Traffic Network

We created a four-way intersection with four incoming roads and four outgoing roads.

### 4.1 Nodes

The file `sumo/nodes.nod.xml` defines five nodes:

- `C`: Central intersection with a traffic light.
- `N`: Northern node.
- `S`: Southern node.
- `E`: Eastern node.
- `W`: Western node.

Node configuration:

```xml
<nodes>
    <node id="C" x="0" y="0" type="traffic_light"/>
    <node id="N" x="0" y="200" type="priority"/>
    <node id="S" x="0" y="-200" type="priority"/>
    <node id="E" x="200" y="0" type="priority"/>
    <node id="W" x="-200" y="0" type="priority"/>
</nodes>
```

### 4.2 Edges

The file `sumo/edges.edg.xml` defines eight edges connecting the outer nodes to the central intersection.

Each edge has:
- One lane.
- A speed limit of 13.89 m/s.

```xml
<edges>
    <edge id="N_in" from="N" to="C" numLanes="1" speed="13.89"/>
    <edge id="S_out" from="C" to="S" numLanes="1" speed="13.89"/>
    <edge id="S_in" from="S" to="C" numLanes="1" speed="13.89"/>
    <edge id="N_out" from="C" to="N" numLanes="1" speed="13.89"/>
    <edge id="E_in" from="E" to="C" numLanes="1" speed="13.89"/>
    <edge id="W_out" from="C" to="W" numLanes="1" speed="13.89"/>
    <edge id="W_in" from="W" to="C" numLanes="1" speed="13.89"/>
    <edge id="E_out" from="C" to="E" numLanes="1" speed="13.89"/>
</edges>
```

### 4.3 Generating the network

We used `netconvert` to generate the network file:

```bash
netconvert \
    --node-files sumo/nodes.nod.xml \
    --edge-files sumo/edges.edg.xml \
    --output-file sumo/intersection.net.xml
```

This successfully generated:

```text
sumo/intersection.net.xml
```

---

## 5. Traffic Routes and Vehicle Flows

The file `sumo/routes.rou.xml` defines four traffic routes:

| Route ID | Direction |
|---|---|
| west_east | West → East |
| east_west | East → West |
| north_south | North → South |
| south_north | South → North |

The current route configuration:

```xml
<routes>
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="13.89"/>

    <route id="west_east" edges="W_in E_out"/>
    <route id="east_west" edges="E_in W_out"/>
    <route id="north_south" edges="N_in S_out"/>
    <route id="south_north" edges="S_in N_out"/>

    <flow id="flow_we" type="car" route="west_east" begin="0" end="600" period="5"/>
    <flow id="flow_ew" type="car" route="east_west" begin="0" end="600" period="5"/>
    <flow id="flow_ns" type="car" route="north_south" begin="0" end="600" period="5"/>
    <flow id="flow_sn" type="car" route="south_north" begin="0" end="600" period="5"/>
</routes>
```

### Vehicle flow settings

| Setting | Value |
|---|---|
| Simulation beginning | 0 seconds |
| Vehicle generation ending | 600 seconds |
| Vehicle generation period | 5 seconds |
| Number of directions | 4 |

Each direction generates vehicles every five seconds during its configured flow period.

---

## 6. Simulation Configuration

The file `sumo/simulation.sumocfg` contains the simulation configuration:

```xml
<configuration>
    <input>
        <net-file value="intersection.net.xml"/>
        <route-files value="routes.rou.xml"/>
    </input>

    <time>
        <begin value="0"/>
        <end value="600"/>
        <step-length value="1"/>
    </time>
</configuration>
```

The simulation uses:
- Network file: `intersection.net.xml`
- Route file: `routes.rou.xml`
- Duration: 600 seconds
- Simulation step length: 1 second

### Testing the simulation

From the project root:

```bash
sumo -c sumo/simulation.sumocfg
```

The simulation successfully completed all 600 seconds.

The output reported approximately 480 total vehicles generated.

---

## 7. SUMO-GUI Setup on macOS

SUMO-GUI initially failed to launch because macOS did not have an accessible X11 display.

We resolved this by installing **XQuartz**, which provides an X11 display server for macOS.

### 7.1 Starting XQuartz

From the regular Mac Terminal:

```bash
open -a XQuartz
```

Wait for XQuartz to start before launching SUMO-GUI.

### 7.2 Configuring DISPLAY

The following command was used to point graphical applications to the XQuartz display:

```bash
export DISPLAY=:0
```

Verify the setting:

```bash
echo $DISPLAY
```

Expected output:

```text
:0
```

### 7.3 Launching SUMO-GUI

From the project root:

```bash
cd ~/Desktop/github/CS175Project

sumo-gui -c sumo/simulation.sumocfg
```

SUMO-GUI successfully launched and displayed:
- The four-way intersection.
- Vehicles traveling through the network.
- Traffic lights.
- The simulation visualization.

### 7.4 Important XQuartz troubleshooting

If SUMO-GUI produces:

```text
FXApp::openDisplay: unable to open display :0
```

Check the following:

1. Make sure XQuartz is running.
2. Make sure `DISPLAY` is set to `:0`.
3. Try opening an X11 application such as:

```bash
/opt/X11/bin/xterm
```

**Important:** Setting `DISPLAY=:0` does not start XQuartz. It only tells applications where to find the display server.

Closing XQuartz shuts down the display server, so SUMO-GUI will no longer be able to connect.

Headless SUMO simulations do not require XQuartz.

### 7.5 Saving GUI visualization settings

The SUMO-GUI appearance was customized, including background and visualization colors.

The customized appearance was successfully configured and saved.

The GUI visualization settings are separate from the main simulation configuration. The simulation configuration controls the network, routes, and timing, while visualization settings control how the simulation looks.

---

## 8. SUMO-RL and Gymnasium Integration

After configuring SUMO, we successfully connected it to SUMO-RL and Gymnasium.

The initial integration test was implemented in `main.py`.

```python
import gymnasium as gym
import sumo_rl

env = gym.make(
    "sumo-rl-v0",
    net_file="sumo/intersection.net.xml",
    route_file="sumo/routes.rou.xml",
    use_gui=False,
    num_seconds=600,
)

obs, info = env.reset()

print("Initial observation:", obs)
print("Observation space:", env.observation_space)
print("Action space:", env.action_space)

for step in range(100):
    action = env.action_space.sample()

    obs, reward, terminated, truncated, info = env.step(action)

    print(f"Step: {step}")
    print(f"Action: {action}")
    print(f"Reward: {reward}")

    if terminated or truncated:
        break

env.close()

print("Simulation completed!")
```

### 8.1 Test results

The environment successfully initialized and ran.

| Property | Result |
|---|---|
| Environment ID | `sumo-rl-v0` |
| Observation shape | `(11,)` |
| Observation space | `Box(0.0, 1.0, (11,), float32)` |
| Action space | `Discrete(2)` |
| Simulation duration | 600 seconds |
| Test steps | 100 |

Initial observation:

```python
[1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
```

The environment completed the random-action test successfully.

**Important:** This was a smoke test, not actual Q-learning training. The random actions were only used to verify that the environment works.

---

## 9. Environment Inspection — Next Technical Step

Before implementing Q-learning, we need to understand exactly what information SUMO-RL provides to the agent.

We need to inspect:
- The observation vector.
- The observation space.
- The available traffic signal actions.
- The number of green phases.
- The incoming lanes.
- How the traffic signal changes between phases.

An inspection script will be used to retrieve this information.

Suggested script: `inspect_env.py`

```python
import gymnasium as gym
import sumo_rl

env = gym.make(
    "sumo-rl-v0",
    net_file="sumo/intersection.net.xml",
    route_file="sumo/routes.rou.xml",
    use_gui=False,
    num_seconds=600,
)

obs, info = env.reset()
base_env = env.unwrapped

print("\n========== ENVIRONMENT DETAILS ==========")

print("\nInitial observation:")
print(obs)

print("\nObservation shape:")
print(obs.shape)

print("\nObservation space:")
print(env.observation_space)

print("\nAction space:")
print(env.action_space)

for ts_id, traffic_signal in base_env.traffic_signals.items():
    print("\nTraffic Light ID:", ts_id)
    print("Number of green phases:", traffic_signal.num_green_phases)

    print("\nIncoming lanes:")
    for lane in traffic_signal.lanes:
        print("-", lane)

    print("\nAvailable green phases:")
    for i, phase in enumerate(traffic_signal.green_phases):
        print(f"Action {i}: {phase.state}")

env.close()
```

Run it from the project root:

```bash
python inspect_env.py
```

The output will help determine the state representation and Q-table design.

We should not assume what each observation index represents until we inspect the actual environment.

---

## 10. Group Setup and Reproducibility

All group members are using macOS.

Since the project works on one machine, we will use that machine as the reference environment and standardize the setup for everyone else.

### 10.1 Diagnostic commands

Every group member should run these commands in their regular Mac Terminal:

```bash
python3 --version
which python3

sumo --version
which sumo

python3 -m pip show gymnasium
python3 -m pip show sumo-rl
```

These commands identify:
- Python version.
- Python executable location.
- SUMO version.
- SUMO executable location.
- Installed Gymnasium version.
- Installed SUMO-RL version.

### 10.2 Check environment variables

Run:

```bash
echo $SUMO_HOME
echo $PYTHONPATH
echo $DISPLAY
```

The working development machine currently uses:

```bash
export SUMO_HOME="/opt/homebrew/lib/python3.14/site-packages/sumo"
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
export DISPLAY=:0
```

These values may differ depending on how SUMO was installed.

Do not blindly copy these paths without checking your own installation.

### 10.3 Common setup problems

| Problem | Possible cause |
|---|---|
| `sumo: command not found` | SUMO is not installed or not in PATH |
| `sumo-gui` cannot open display | XQuartz is not running or DISPLAY is incorrect |
| `No module named gymnasium` | Gymnasium is not installed in the active Python environment |
| `No module named sumo_rl` | SUMO-RL is not installed in the active Python environment |
| SUMO tools cannot be found | SUMO_HOME or PYTHONPATH is incorrect |
| Network file not found | Incorrect working directory or file path |
| Invalid XML configuration | Incorrect XML syntax or configuration |

### 10.4 Standardization goals

To make the project reproducible across all group members, we should eventually maintain:

- A complete `requirements.txt`.
- A consistent Python environment.
- A step-by-step macOS installation guide.
- A SUMO installation verification script.
- A SUMO-RL integration test.

We should compare everyone's diagnostic outputs before deciding on exact dependency versions.

---

## 11. Current Project Status

### Completed

- [x] Installed SUMO.
- [x] Verified SUMO installation.
- [x] Configured SUMO_HOME and PYTHONPATH.
- [x] Created the four-way intersection.
- [x] Generated the SUMO network using `netconvert`.
- [x] Created four traffic routes.
- [x] Configured vehicle flows.
- [x] Configured the 600-second simulation.
- [x] Successfully ran the headless SUMO simulation.
- [x] Installed and tested SUMO-RL.
- [x] Integrated SUMO-RL with Gymnasium.
- [x] Verified the observation and action spaces exist.
- [x] Successfully ran random actions through the environment.
- [x] Installed XQuartz.
- [x] Configured XQuartz to work with SUMO-GUI.
- [x] Successfully launched SUMO-GUI.
- [x] Customized and saved SUMO-GUI visualization colors.

### In Progress

- [ ] Standardize the setup across all group members.
- [ ] Collect diagnostic outputs from teammates.
- [ ] Inspect the SUMO-RL observation and action details.
- [ ] Finalize the Q-learning state representation.

### Upcoming Tasks

1. Finish environment inspection.
2. Design the Q-learning state representation.
3. Implement the Q-learning agent in `agent/q_learning.py`.
4. Implement the training loop in `training/train.py`.
5. Implement a fixed-time traffic signal controller in `controllers/fixed_time.py`.
6. Develop evaluation metrics in `evaluation/metrics.py`.
7. Compare the Q-learning agent against the fixed-time baseline in `evaluation/compare.py`.
8. Save training results in `results/`.
9. Analyze and document the results.

---

## 12. Running the Project

All commands below should be run from the project root:

```bash
cd ~/Desktop/github/CS175Project
```

### Run headless SUMO

```bash
sumo -c sumo/simulation.sumocfg
```

### Run SUMO-GUI

Make sure XQuartz is running first:

```bash
open -a XQuartz
```

Then:

```bash
export DISPLAY=:0

sumo-gui -c sumo/simulation.sumocfg
```

### Run the SUMO-RL integration test

```bash
python main.py
```

### Run the environment inspection script

Once created:

```bash
python inspect_env.py
```

---

## 13. Current Milestone

**SUMO installation, traffic network creation, SUMO-RL integration, and GUI configuration are complete on the reference Mac.**

The immediate priorities are:

1. Help all group members get the project running on their Macs.
2. Inspect the SUMO-RL environment.
3. Design and implement the tabular Q-learning agent.

The next major development milestone is a working Q-learning agent that can control the intersection's traffic signals and be evaluated against a fixed-time controller.
