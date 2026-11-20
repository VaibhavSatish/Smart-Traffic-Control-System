from agent.q_learning import QLearningTrafficAgent

agent = QLearningTrafficAgent()
state = (0,0,0,0,0,0)
next_state = (1,1,0,1,0,0)
action = agent.choose_action(state)
print("Chosen Action: ", action)
print("Initial Q-values: ", agent.q_table[state])
agent.learn(state, action, 1.0, next_state, True)
print("Updated Q-values: ", agent.q_table[state])
print("Exploration Rate before decay", agent.epsilon)
agent.decay_exploration()
print("Exploration Rate after decay", agent.epsilon)