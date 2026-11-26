def custom_reward(traffic_signal):
    # Waiting time
    current_waiting_time = sum(
        traffic_signal.get_accumulated_waiting_time_per_lane()
    )

    previous_waiting_time = getattr(
        traffic_signal, "_previous_custom_waiting", 0.0
    )

    waiting_time_delta = current_waiting_time - previous_waiting_time
    traffic_signal._previous_custom_waiting = current_waiting_time

    # Queue length
    queue_length = traffic_signal.get_total_queued()

    # Throughput
    current_vehicles = set()

    for lane in traffic_signal.out_lanes:
        current_vehicles.update(
            traffic_signal.sumo.lane.getLastStepVehicleIDs(lane)
        )

    seen_vehicles = getattr(
        traffic_signal, "_seen_out_vehicles", set()
    )

    new_vehicles = current_vehicles - seen_vehicles
    traffic_signal._seen_out_vehicles = seen_vehicles | current_vehicles

    throughput = len(new_vehicles)

    # Signal switching penalty
    current_phase = traffic_signal.green_phase

    previous_phase = getattr(
        traffic_signal, "_previous_custom_phase", current_phase
    )

    switching_penalty = int(current_phase != previous_phase)
    traffic_signal._previous_custom_phase = current_phase

    # Individual components
    waiting_component = -waiting_time_delta
    queue_component = -queue_length
    throughput_component = throughput
    switching_component = -switching_penalty

    # Reward
    reward = (
        waiting_component
        + queue_component
        + throughput_component
        + switching_component
    )

    # print(
    #     f"Waiting: {waiting_component} | "
    #     f"Queue: {queue_component} | "
    #     f"Throughput: {throughput_component} | "
    #     f"Switching: {switching_component} | "
    #     f"Total: {reward}"
    # )

    return reward