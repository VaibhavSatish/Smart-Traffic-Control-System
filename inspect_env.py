
import gymnasium as gym
import sumo_rl
from agent.q_learning import get_state
env = gym.make(
    "sumo-rl-v0",
    net_file="sumo/intersection.net.xml",
    route_file="sumo/routes.rou.xml",
    use_gui=False,
    num_seconds=600,
)

obs, info = env.reset()

lane_names = ["North", "East", "South", "West"]

for step in range(20):
    action = step % 2

    obs, reward, terminated, truncated, info = env.step(action)

    print(f"\n========== STEP {step + 1} ==========")
    print("Action:", action)
    print("Reward:", reward)

    print("Current phase:", obs[0:2])
    print("Minimum green:", obs[2])

    print("\nLane densities:")
    for i, lane in enumerate(lane_names):
        print(f"{lane}: {obs[3 + i]:.3f}")

    print("\nLane queues:")
    for i, lane in enumerate(lane_names):
        print(f"{lane}: {obs[7 + i]:.3f}")

    if terminated or truncated:
        break

    state = get_state(obs)
    print("Discrete State: ", state)

env.close()
