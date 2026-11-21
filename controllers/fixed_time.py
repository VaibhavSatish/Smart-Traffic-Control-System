
def fixed_time_action(step, phase_duration_steps=6):

    cycle_length = phase_duration_steps * 2

    position = step % cycle_length

    if position < phase_duration_steps:
        return 0
    else:
        return 1
