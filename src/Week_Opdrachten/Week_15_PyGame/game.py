import pygame
from agent import Agent
from grid_world import GridWorld
from q_learning_agent import QLearningAgent

class Game:
    def __init__(self):
        self.grid_world = GridWorld()
        self.agent = Agent(1, 1, self.grid_world)  # Start op positie (1,1)
        self.q_agent = QLearningAgent(self.grid_world)
        self.use_q_agent = False
        self.running = True

    def reset_environment(self): # Complete Environment Reset
        self.agent.reset_position()
        self.q_agent.q_table = {}
        self.q_agent.epsilon = 0.2
        self.use_q_agent = False             

        print("Environment is volledig gereset")
    
    def handle_input(self): # Behandel keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_environment()
                elif event.key == pygame.K_t:
                    print("Agent trainen met Q-Learning")
                    self.train_agent(episodes=1000)
                    print("Training succesvol!")
                    self.use_q_agent = True
                    self.agent.reset_position()
                elif event.key == pygame.K_1:
                    self.q_agent.adjust_learning_rate(-0.05)
                elif event.key == pygame.K_2:
                    self.q_agent.adjust_learning_rate(0.05)
                elif event.key == pygame.K_3:
                    self.q_agent.adjust_discount_factor(-0.05)
                elif event.key == pygame.K_4:
                    self.q_agent.adjust_discount_factor(0.05)
                elif event.key == pygame.K_5:
                    self.q_agent.adjust_epsilon(-0.05)
                elif event.key == pygame.K_6:
                    self.q_agent.adjust_epsilon(0.05)

        keys = pygame.key.get_pressed()
        
        # Beweging controls: W = Up, A = Left, S = Down, D = Right
        if keys[pygame.K_a]:
            self.agent.move_agent("left")
        if keys[pygame.K_d]:
            self.agent.move_agent("right")
        if keys[pygame.K_w]:
            self.agent.move_agent("up")
        if keys[pygame.K_s]:
            self.agent.move_agent("down")
    
    def check_win_condition(self): # Check of het spel gewonnen is
        if self.agent.has_reached_goal():
            print("Gewonnen!")
            self.running = False

    def train_agent(self, episodes=1000):
        for episode in range(episodes):
            self.agent.reset_position()
            done = False

            while not done:
                state = (self.agent.x, self.agent.y)
                action = self.q_agent.choose_action(state)
                self.agent.move_agent(action)

                reward = self.grid_world.get_reward((self.agent.x, self.agent.y))

                next_state = (self.agent.x, self.agent.y)
                self.q_agent.update_q_value(state, action, reward, next_state)

                done = self.agent.has_reached_goal()

            print(f"Episode {episode + 1}/{episodes} voltooid")


    
    def run(self): # Main game loop
        while self.running:
            pygame.time.delay(100)
            
            # Handle input
            if self.use_q_agent:
                state = (self.agent.x, self.agent.y)
                action = self.q_agent.choose_action(state)
                self.agent.move_agent(action)
            else:
                self.handle_input()

            

            # Clear screen
            self.grid_world.screen.fill(self.grid_world.white)
            
            # Draw everything
            self.grid_world.draw_maze()
            self.grid_world.draw_goal()
            self.agent.draw_agent()

            if self.use_q_agent:
                self.grid_world.draw_q_values_simple(self.q_agent.q_table)
            
            # Check win condition
            self.check_win_condition()
            
            # Update display
            pygame.display.update()
        
        # Quit
        pygame.quit()

# Start het spel
if __name__ == "__main__":
    game = Game()
    game.run()