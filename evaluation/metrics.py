
import gymnasium as gym
import sumo_rl


env = gym.make(
    "sumo-rl-v0",
    net_file="sumo/intersection.net.xml",
    route_file="sumo/routes.rou.xml",
    use_gui=False,
    num_seconds=600,
)

observation, info = env.reset()

print("Initial info keys:", info.keys())

for step in range(10):

    action = env.action_space.sample()

    observation, reward, terminated, truncated, info = env.step(action)

    print(f"\nStep {step + 1}")
    print("Reward:", reward)
    print("Info:", info)

    if terminated or truncated:
        break

env.close()
