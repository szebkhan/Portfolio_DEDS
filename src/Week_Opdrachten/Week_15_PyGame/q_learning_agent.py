import random

class QLearningAgent():
    def __init__(self, grid_world, agent, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.grid_world = grid_world
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.agent = agent

        self.actions = ["up", "down", "left", "right"]

    def get_q(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}
        return self.q_table[state][action]

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            self.ensure_state_exists(state)
            return max(self.q_table[state], key=self.q_table[state].get)

    def ensure_state_exists(self, state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}

    def update_q_value(self, state, action, reward, next_state):
        self.ensure_state_exists(state)
        self.ensure_state_exists(next_state)

        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())

        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def adjust_learning_rate(self, change): # Learning rate veranderen
        self.alpha = max(0.01, min(1.0, self.alpha + change))
        print(f"Learning rate veranderd naar: {self.alpha:.2f}")

    def adjust_discount_factor(self, change): # Discount factor veranderen
        self.gamma = max(0.1, min(1.0, self.gamma + change))
        print(f"Discount factor veranderd naar: {self.gamma:.2f}")

    def adjust_epsilon(self, change): # Exploration rate veranderen
        self.epsilon = max(0.01, min(1.0, self.epsilon + change))
        print(f"Exploration rate veranderd naar: {self.epsilon:.2f}")

    def train(self, episodes=500):
        for episode in range(episodes):
            self.agent.reset_position()
            done = False

            while not done:
                state = (self.agent.x, self.agent.y)
                action = self.choose_action(state)
                self.agent.move_agent(action)

                reward = self.grid_world.get_reward((self.agent.x, self.agent.y))

                next_state = (self.agent.x, self.agent.y)
                self.update_q_value(state, action, reward, next_state)

                done = self.agent.has_reached_goal()

            print(f"Episode {episode + 1}/{episodes} voltooid")

    def learn_step(self):

        state = (self.agent.x, self.agent.y)
        action = self.choose_action(state)
        self.agent.move_agent(action)

        reward = self.grid_world.get_reward((self.agent.x, self.agent.y))
        next_state = (self.agent.x, self.agent.y)

        self.update_q_value(state, action, reward, next_state)

        if self.agent.has_reached_goal():
            self.epsilon = max(0.01, self.epsilon * 0.99)
