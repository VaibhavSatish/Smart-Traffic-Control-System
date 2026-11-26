def custom_reward(traffic_signal):
    waiting_time = sum(
        traffic_signal.get_accumulated_waiting_time_per_lane()
    )

    queue_length = traffic_signal.get_total_queued()

    reward = -waiting_time - queue_length

    return reward
