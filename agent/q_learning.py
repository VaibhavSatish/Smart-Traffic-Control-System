def discretize_queue(queue) -> int:
    """
    Convert a normalized queue value into
    one of three categories.
    """
    if queue < 0.05: #tweak this threshold to make agent better
        return 0
    elif queue < 0.15: #tweak this threshold to make agent better
        return 1
    else:
        return 2

def get_state(observation) -> tuple:
    """
    Convert a SUMO-RL observation into
    a discrete Q-learning state.
    """
    cur_phase = int(observation[0:2].argmax())
    queues = observation[7:11]
    discrete_queue = tuple(discretize_queue(queue) for queue in queues)

    return (cur_phase, ) + discrete_queue