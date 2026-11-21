## 2. Installing dependencies
```bash
pip install -r requirements.txt
```
OR
```bash
pip3 install -r requirements.txt
```

If install Sumo-rl errors out trying following the steps below first and then doing the above!

## 3. Installing and Configuring SUMO on macOS

This section describes the installation process for group members
setting up the project on their Macs.

### 3.1 Install Homebrew

Homebrew is a package manager for macOS.

Check whether it is installed:

``` bash
brew --version
```

If it is not installed, follow the official instructions at
[brew.sh](https://brew.sh/).

### 3.2 Install SUMO

Install SUMO using Homebrew:

``` bash
brew install sumo
```

Verify the installation:

``` bash
sumo --version
sumo-gui --version
which sumo
which sumo-gui
```

On the reference Mac:

-   SUMO version: **1.28.0**
-   SUMO executable: `/opt/homebrew/bin/sumo`

The executable location and version may differ on other Macs.

### 3.3 Find the SUMO tools directory

The reference Mac's SUMO tools directory was:

``` text
/opt/homebrew/lib/python3.14/site-packages/sumo
```

This path is specific to the reference Mac. Do not assume it will be
identical on every computer. Each teammate should locate their own SUMO
installation and tools directory.

### 3.4 Configure SUMO environment variables

On the reference Mac, the following variables were used:

``` bash
export SUMO_HOME="/opt/homebrew/lib/python3.14/site-packages/sumo"
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
```

These variables allow Python to locate SUMO's tools, including tools
used by SUMO-RL.

Use the correct path for the local installation.

### 3.5 Make environment variables persistent (Zsh)

To avoid re-entering the variables in every new Terminal session, open
the Zsh configuration file:

``` bash
nano ~/.zshrc
```

Add the appropriate `SUMO_HOME` and `PYTHONPATH` exports. For the
reference Mac:

``` bash
export SUMO_HOME="/opt/homebrew/lib/python3.14/site-packages/sumo"
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
```

Save the file, exit the editor, and reload the configuration:

``` bash
source ~/.zshrc
```

Verify the variables:

``` bash
echo "$SUMO_HOME"
echo "$PYTHONPATH"
```

------------------------------------------------------------------------

## 4. Installing and Configuring XQuartz for SUMO-GUI

SUMO's graphical interface uses the X11 windowing system. On macOS,
**XQuartz** provides the X11 display server needed to run SUMO-GUI.

### 4.1 Install and start XQuartz

Download and install XQuartz from
[xquartz.org](https://www.xquartz.org/).

Start it from the regular Mac Terminal:

``` bash
open -a XQuartz
```

Wait for XQuartz to start before launching SUMO-GUI.

### 4.2 Configure the display

In the regular Mac Terminal, set:

``` bash
export DISPLAY=:0
```

Verify:

``` bash
echo "$DISPLAY"
```

On the reference Mac, the expected value was:

``` text
:0
```

This tells graphical applications where to find the XQuartz display
server. It does **not** start XQuartz.

### 4.3 Test the XQuartz display

Run:

``` bash
/opt/X11/bin/xterm
```

If an xterm window opens, the X11 display connection is working.

### 4.4 Make DISPLAY persistent (optional)

If desired, add the following to `~/.zshrc`:

``` bash
export DISPLAY=:0
```

Then reload the configuration:

``` bash
source ~/.zshrc
```

This setting assumes XQuartz is running and available at `:0`. If
XQuartz is closed, graphical applications cannot connect even if
`DISPLAY` is set.

### 4.5 Important XQuartz behavior

Keep XQuartz running while using SUMO-GUI. Closing XQuartz shuts down
the display server.

If SUMO-GUI displays:

``` text
FXApp::openDisplay: unable to open display :0
```

check that:

1.  XQuartz is running.
2.  `echo "$DISPLAY"` reports the display configured for XQuartz (on the
    reference Mac, `:0`).
3.  `/opt/X11/bin/xterm` can open.

Headless SUMO simulations do not require XQuartz.

------------------------------------------------------------------------

## 5. Creating the SUMO Traffic Network

We created a four-way intersection with four incoming roads and four
outgoing roads.

### 5.1 Nodes

The file `sumo/nodes.nod.xml` defines five nodes:

-   `C`: central intersection with a traffic light
-   `N`: northern node
-   `S`: southern node
-   `E`: eastern node
-   `W`: western node

The node configuration is:

``` xml
<nodes>
    <node id="C" x="0" y="0" type="traffic_light"/>
    <node id="N" x="0" y="200" type="priority"/>
    <node id="S" x="0" y="-200" type="priority"/>
    <node id="E" x="200" y="0" type="priority"/>
    <node id="W" x="-200" y="0" type="priority"/>
</nodes>
```

### 5.2 Edges

The file `sumo/edges.edg.xml` defines eight edges connecting the outer
nodes to the central intersection.

Each edge has one lane and a speed limit of 13.89 m/s.

``` xml
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

### 5.3 Generate the network

From the project root, run:

``` bash
netconvert \
    --node-files sumo/nodes.nod.xml \
    --edge-files sumo/edges.edg.xml \
    --output-file sumo/intersection.net.xml
```

This generates `sumo/intersection.net.xml`.

------------------------------------------------------------------------

## 6. Traffic Routes and Vehicle Flows

The file `sumo/routes.rou.xml` defines four traffic routes:

  Route ID        Direction
  --------------- ---------------
  `west_east`     West → East
  `east_west`     East → West
  `north_south`   North → South
  `south_north`   South → North

The current route configuration is:

``` xml
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

Each direction generates vehicles every five seconds during its
configured flow period.

  Setting                Value
  ---------------------- -------------
  Flow beginning         0 seconds
  Flow ending            600 seconds
  Generation period      5 seconds
  Number of directions   4

------------------------------------------------------------------------

## 7. Simulation Configuration and Testing

The file `sumo/simulation.sumocfg` contains the simulation
configuration:

``` xml
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

-   Network file: `intersection.net.xml`
-   Route file: `routes.rou.xml`
-   Duration: 600 seconds
-   Simulation step length: 1 second

### Run the headless simulation

From the project root:

``` bash
sumo -c sumo/simulation.sumocfg
```

The simulation successfully completed all 600 seconds on the reference
Mac. The output reported approximately 480 total vehicles generated.

### Run the simulation with SUMO-GUI

First, start XQuartz and configure `DISPLAY` if needed:

``` bash
open -a XQuartz
export DISPLAY=:0
```

Then run:

``` bash
cd ~/Desktop/github/CS175Project
sumo-gui -c sumo/simulation.sumocfg
```

------------------------------------------------------------------------

## 8. SUMO-GUI Visualization Settings

The SUMO-GUI appearance was customized, including the background and
visualization colors. The customized appearance was successfully saved.

The visualization settings are separate from the main simulation
settings:

-   `simulation.sumocfg` configures the network, routes, and simulation
    timing.
-   GUI view settings control how the simulation is displayed.

The GUI colors are considered complete on the reference Mac. The saved
GUI configuration file is present in the project structure as
`sumo/gui_settings.sumocfg`.

------------------------------------------------------------------------

## 9. SUMO-RL and Gymnasium Integration

### 9.1 Install SUMO-RL

Install SUMO-RL with pip:

```bash
pip3 install sumo-rl
```

On the reference Mac, the regular installation command did not work
because the Homebrew-managed Python environment blocked package
installation. The workaround used was:

```bash
pip3 install sumo-rl --break-system-packages
```

The `--break-system-packages` flag bypasses Python's externally-managed
environment protection (PEP 668). This is a workaround, not the preferred
approach for every setup. A Python virtual environment is safer because
it keeps project dependencies separate from the system/Homebrew Python
installation.

After installation, verify that the package is available to the Python
interpreter you plan to use:

```bash
python3 -m pip show sumo-rl
python3 -c "import sumo_rl; print('SUMO-RL imported successfully!')"
```

**Important:** Installing `sumo-rl` and configuring SUMO are separate
steps. If Python reports that `SUMO_HOME` is not set, configure
`SUMO_HOME` and `PYTHONPATH` as described in Section 3. The pip flag
does not fix SUMO environment-variable errors.

After configuring SUMO, we successfully connected it to SUMO-RL and
Gymnasium.

The initial integration test was implemented in `main.py`:

``` python
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

### 9.2 Test results

The environment successfully initialized and ran.

  Property                         Result
  -------------------------------- ---------------------------------
  Environment ID                   `sumo-rl-v0`
  Observation shape                `(11,)`
  Observation space                `Box(0.0, 1.0, (11,), float32)`
  Action space                     `Discrete(2)`
  Simulation duration configured   600 seconds
  Test steps                       100

The initial observation was:

``` python
[1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
```

The environment completed the random-action test successfully.

**Note:** This was a smoke test to verify that SUMO-RL and Gymnasium
work together. It was not Q-learning training; the actions were sampled
randomly.

------------------------------------------------------------------------

## 10. Inspecting the SUMO-RL Environment

Before implementing Q-learning, we need to understand exactly what
information SUMO-RL provides to the agent.

The inspection should identify:

-   The observation vector and its shape
-   The observation space
-   The available traffic signal actions
-   The number of green phases
-   The incoming lanes
-   The available green-phase states

The following inspection script was proposed as `inspect_env.py`:

``` python
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

``` bash
python inspect_env.py
```

The output will help determine the state representation and Q-table
design. We should not assume what each observation index represents
until the environment has been inspected.

------------------------------------------------------------------------

## 11. Group Setup and Reproducibility

All group members are using macOS. The reference Mac is the working
setup that the rest of the team can compare against.

### 11.1 Diagnostic commands

Every group member should run these commands in their regular Mac
Terminal:

``` bash
python3 --version
which python3

sumo --version
which sumo

python3 -m pip show gymnasium
python3 -m pip show sumo-rl
```

These commands report:

-   Python version and executable location
-   SUMO version and executable location
-   Installed Gymnasium version
-   Installed SUMO-RL version

### 11.2 Check environment variables

Run:

``` bash
echo "$SUMO_HOME"
echo "$PYTHONPATH"
echo "$DISPLAY"
```

The reference Mac currently uses:

``` bash
export SUMO_HOME="/opt/homebrew/lib/python3.14/site-packages/sumo"
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
export DISPLAY=:0
```

These values may differ depending on how SUMO was installed. Teammates
should verify their own installation paths rather than copying the
reference paths blindly.

### 11.3 Common setup problems

  -----------------------------------------------------------------------
  Error or problem                    Possible cause / first check
  ----------------------------------- -----------------------------------
  `brew: command not found`           Homebrew is not installed or its
                                      PATH is not configured

  `sumo: command not found`           SUMO is not installed or its
                                      executable is not in PATH

  `sumo-gui: command not found`       Check the SUMO installation and
                                      PATH

  `FXApp::openDisplay`                XQuartz is not running or `DISPLAY`
                                      is incorrect

  `No module named gymnasium`         Gymnasium is missing from the
                                      active Python environment

  `No module named sumo_rl`           SUMO-RL is missing from the active
                                      Python environment

  `No module named traci`             Check `SUMO_HOME`, `PYTHONPATH`,
                                      and the active Python environment

  SUMO tools cannot be found          Check `SUMO_HOME` and `PYTHONPATH`

  Network file not found              Check the working directory and
                                      file paths

  Invalid XML configuration           Check XML syntax and configuration
                                      file contents
  -----------------------------------------------------------------------

### 11.4 Standardization goals

To make the project reproducible across all group members, the team
should maintain:

-   A complete and tested `requirements.txt`
-   A consistent Python environment and package versions
-   A step-by-step macOS installation guide
-   A SUMO installation verification process
-   A SUMO-RL integration test

Compare everyone's diagnostic outputs before deciding which exact
dependency versions to standardize.

------------------------------------------------------------------------

## 12. Current Project Status

### Completed

-   [x] Installed SUMO on the reference Mac.
-   [x] Verified the SUMO installation.
-   [x] Configured `SUMO_HOME` and `PYTHONPATH`.
-   [x] Created the four-way intersection.
-   [x] Generated the SUMO network using `netconvert`.
-   [x] Created four traffic routes.
-   [x] Configured vehicle flows.
-   [x] Configured the 600-second simulation.
-   [x] Successfully ran the headless SUMO simulation.
-   [x] Installed and tested SUMO-RL.
-   [x] Integrated SUMO-RL with Gymnasium.
-   [x] Verified that the observation and action spaces are available.
-   [x] Successfully ran random actions through the environment.
-   [x] Installed XQuartz.
-   [x] Configured XQuartz to work with SUMO-GUI.
-   [x] Successfully launched SUMO-GUI.
-   [x] Customized and saved SUMO-GUI visualization colors.

### In Progress

-   [ ] Standardize the setup across all group members.
-   [ ] Collect diagnostic outputs from teammates.
-   [ ] Inspect the SUMO-RL observation and action details.
-   [ ] Finalize the Q-learning state representation.

### Upcoming Tasks

1.  Finish inspecting the SUMO-RL environment.
2.  Design the Q-learning state representation.
3.  Implement the Q-learning agent in `agent/q_learning.py`.
4.  Implement the training loop in `training/train.py`.
5.  Implement a fixed-time traffic signal controller in
    `controllers/fixed_time.py`.
6.  Develop evaluation metrics in `evaluation/metrics.py`.
7.  Compare the Q-learning agent against the fixed-time baseline in
    `evaluation/compare.py`.
8.  Save training results in `results/`.
9.  Analyze and document the results.

------------------------------------------------------------------------

## 13. Quick Reference: Running the Project

Run commands from the project root:

``` bash
cd ~/Desktop/github/CS175Project
```

### Run headless SUMO

``` bash
sumo -c sumo/simulation.sumocfg
```

### Run SUMO-GUI

Make sure XQuartz is running:

``` bash
open -a XQuartz
export DISPLAY=:0
```

Then:

``` bash
sumo-gui -c sumo/simulation.sumocfg
```

### Run the SUMO-RL integration test

``` bash
python main.py
```

### Run the environment inspection script

Once `inspect_env.py` has been created:

``` bash
python inspect_env.py
```

------------------------------------------------------------------------

## Official Resources

-   [Homebrew](https://brew.sh/)
-   [SUMO Documentation](https://sumo.dlr.de/docs/)
-   [SUMO Installation
    Documentation](https://sumo.dlr.de/docs/Installing/index.html)
-   [XQuartz](https://www.xquartz.org/)
-   [Gymnasium Documentation](https://gymnasium.farama.org/)
-   [SUMO-RL Repository](https://github.com/LucasAlegre/sumo-rl)
