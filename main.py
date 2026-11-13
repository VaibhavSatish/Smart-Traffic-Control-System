
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

