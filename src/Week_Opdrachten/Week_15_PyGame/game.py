import pygame
import sys
from agent import Agent
from grid_world import GridWorld
from q_learning_agent import QLearningAgent

class Game:
    def __init__(self):
        self.grid_world = GridWorld()
        self.agent = Agent(0, 0, self.grid_world)  # Start op positie (1,1)
        self.q_agent = QLearningAgent(self.grid_world, self.agent)
        self.user = "MANUAL"
        self.running = True
        self.episode = 0
        self.steps = 0

    def reset_environment(self):
        self.user = "MANUAL" # Complete Environment Reset
        self.agent.reset_position()
        self.q_agent.q_table = {}
        self.q_agent.epsilon = 0.2
        self.episode = 0
        self.steps = 0

        print("Environment is volledig gereset")
    
    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_environment()
                elif event.key == pygame.K_t:
                    self.user = "AGENT"
                    pygame.time.delay(5)
                elif event.key == pygame.K_y:
                    self.user = "MANUAL"
                    pygame.time.delay(100)
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
    
    def handle_input(self): # Behandel keyboard input
        if self.user == "MANUAL":
            pygame.time.delay(100)

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
    
    def run(self): # Main game loop
        while self.running:

            pygame.display.set_caption(f"{self.user} | Episode {self.episode} | Steps: {self.steps}")

            self.controls()

            # Handle input
            if self.user == "AGENT":
                self.q_agent.learn_step()
                self.steps += 1
            else:
                self.handle_input()

            # Clear screen
            self.grid_world.screen.fill(self.grid_world.white)
            
            # Draw everything
            self.grid_world.draw_maze()
            self.grid_world.draw_goal()
            self.agent.draw_agent()

            if self.user == "AGENT":
                self.grid_world.draw_q_values(self.q_agent.q_table)
            
            # Check win condition
            if self.agent.has_reached_goal() and self.user == "AGENT":
                self.agent.reset_position()
                self.episode += 1
                self.steps = 0

            if self.steps > 350:
                self.agent.reset_position()
                self.episode += 1
                self.steps = 0
            
            # Update display
            pygame.display.update()
        
        # Quit
        pygame.quit()
        

# Start het spel
if __name__ == "__main__":
    game = Game()
    game.run()