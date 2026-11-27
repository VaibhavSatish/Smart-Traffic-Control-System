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

traffic_signal = env.unwrapped.traffic_signals["C"]
sumo = traffic_signal.sumo

passed_vehicles = set()

for step in range(50):
    obs, reward, terminated, truncated, info = env.step(0)

    current_vehicles = set()

    for lane in traffic_signal.out_lanes:
        current_vehicles.update(sumo.lane.getLastStepVehicleIDs(lane))

    new_vehicles = current_vehicles - passed_vehicles
    passed_vehicles.update(new_vehicles)

    print(
        f"Step {step + 1}: "
        f"New vehicles: {len(new_vehicles)} | "
        f"Cumulative throughput: {len(passed_vehicles)}"
    )

    if terminated or truncated:
        break

env.close()