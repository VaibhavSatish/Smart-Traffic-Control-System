import numpy as np
from collections import defaultdict

def discretize_queue(queue):
    if queue < 0.05:
        return 0
    elif queue < 0.15:
        return 1
    else:
        return 2


def get_state(observation):
    current_phase = int(observation[0:2].argmax())
    min_green = int(observation[2])

    queues = observation[7:11]

    discrete_queues = tuple(
        discretize_queue(queue) for queue in queues
    )

    return (current_phase, min_green) + discrete_queues

class QLearningTrafficAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay
        self.epsilon_min = min_exploration_rate
        self.q_table = defaultdict(lambda: np.zeros(2))

    def choose_action(self, state):
        rng = np.random.default_rng()
        if rng.random() < self.epsilon:
            return np.random.randint(2)
        return int(np.argmax(self.q_table[state]))

    def learn(self, state, action, reward, next_state, done):
        cur_q = self.q_table[state][action]
        if done:
            target = reward
        else:
            future_q = np.max(self.q_table[next_state])
            target = reward + self.gamma * future_q

        self.q_table[state][action] = (cur_q + self.lr * (target-cur_q))

    def decay_exploration(self):
        self.epsilon = max(self.epsilon_min, self.epsilon*self.epsilon_decay)