import gymnasium as gym
import sumo_rl
from agent.custom_reward import custom_reward

env = gym.make(
    "sumo-rl-v0",
    net_file="sumo/intersection.net.xml",
    route_file="sumo/routes.rou.xml",
    use_gui=False,
    num_seconds=50,
    reward_fn=custom_reward,
)

obs, info = env.reset()

for step in range(10):
    action = 0 if step < 5 else 1

    obs, reward, terminated, truncated, info = env.step(action)

    print(f"Step {step + 1} | Action: {action} | Environment reward: {reward}")

    if terminated or truncated:
        break

env.close()