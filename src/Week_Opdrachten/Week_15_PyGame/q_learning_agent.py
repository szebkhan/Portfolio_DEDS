import random

class QLearningAgent():
    def __init__(self, grid_world, agent, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.grid_world = grid_world
        self.alpha = alpha # Learning Rate, hoe snel leert de Agent
        self.gamma = gamma # Discount Factor, Hoe belangrijk zijn future rewards
        self.epsilon = epsilon # Kans op random action vs best action (exploration vs exploitation)
        self.q_table = {}
        self.agent = agent

        self.actions = ["up", "down", "left", "right"] # Alle mogelijke acties die ondernomen kunnen worden

    def choose_action(self, state):
        if random.random() < self.epsilon: # Random actie wordt ondernomen -> er is sprake van exploration
            return random.choice(self.actions)
        else:
            self.ensure_state_exists(state) # De best known actie wordt ondernomen -> Hij exploit zijn kennis (exploitation)
            return max(self.q_table[state], key=self.q_table[state].get)

    def ensure_state_exists(self, state): # Check of gegeven state bestaat in q table (errors voorkomen)
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}

    def update_q_value(self, state, action, reward, next_state):
        self.ensure_state_exists(state)
        self.ensure_state_exists(next_state)

        current_q = self.q_table[state][action] # Sla huidige q values op
        max_next_q = max(self.q_table[next_state].values()) # Pak beste q value

        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q) #Q learning formule toepassen
        self.q_table[state][action] = new_q # Nieuwe q values opslaan in q table

    def adjust_learning_rate(self, change): # Learning rate veranderen
        self.alpha = max(0.01, min(1.0, self.alpha + change))
        print(f"Learning rate veranderd naar: {self.alpha:.2f}")

    def adjust_discount_factor(self, change): # Discount factor veranderen
        self.gamma = max(0.1, min(1.0, self.gamma + change))
        print(f"Discount factor veranderd naar: {self.gamma:.2f}")

    def adjust_epsilon(self, change): # Exploration rate veranderen
        self.epsilon = max(0.01, min(1.0, self.epsilon + change))
        print(f"Exploration rate veranderd naar: {self.epsilon:.2f}")

    def train(self, episodes=500): # Train achter de scenes met 500 episodes
        for episode in range(episodes):
            self.agent.reset_position() # Start bij begin
            done = False

            while not done:
                state = (self.agent.x, self.agent.y)
                action = self.choose_action(state)
                self.agent.move_agent(action) # Sla state en actie op, beweeg agent op basis van actie.

                reward = self.grid_world.get_reward((self.agent.x, self.agent.y)) # krijg reward op basis van actie

                next_state = (self.agent.x, self.agent.y) # Bewaar nieuwe state
                self.update_q_value(state, action, reward, next_state) # update q value op basis van nieuwe actie

                done = self.agent.has_reached_goal()

            print(f"Episode {episode + 1}/{episodes} voltooid")

    def learn_step(self): # Zelfde als train, maar gaat in stapsgewijs (geen fixed amount of episodes. function beweegt maar 1 stap per call.)

        state = (self.agent.x, self.agent.y)
        action = self.choose_action(state)
        self.agent.move_agent(action)

        reward = self.grid_world.get_reward((self.agent.x, self.agent.y))
        next_state = (self.agent.x, self.agent.y)

        self.update_q_value(state, action, reward, next_state)

        if self.agent.has_reached_goal():
            self.epsilon = max(0.01, self.epsilon * 0.99)
