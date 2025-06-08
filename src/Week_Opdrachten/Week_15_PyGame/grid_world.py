import pygame
import numpy as np
import random

class GridWorld:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.rows = 10
        self.cols = 10
        self.cell_width = self.screen_width // self.cols
        self.cell_height = self.screen_height // self.rows
        
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.black = (0, 0, 0)
        self.gray = (150, 150, 150)
        self.purple = (255, 0, 255)
        
        # self.maze = [
        #     [0, 1, 0, 0, 0, 1, 0, 0, 2, 0],
        #     [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        #     [0, 0, 0, 1, 0, 0, 2, 0, 1, 0],
        #     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 1, 2, 1, 0, 1, 0, 1, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        #     [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 1, 0, 0, 0, 1, 0, 2],
        #     [0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
        # ]

        self.maze = self.generate_maze()

        # Goal position
        self.goal_row = self.rows - 1
        self.goal_col = self.cols - 1
    
    def generate_maze(self):   
        maze = []

        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                tile = random.choices([0, 1, 2], weights=[0.75, 0.15, 0.10])[0]
                row.append(tile)
            maze.append(row)

        maze[0][0] = 0
        maze[self.rows - 1][self.cols - 1] = 0
        return maze

    def draw_maze(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) == (0, 0):
                    color = self.purple
                else:
                    cell = self.maze[row][col]
                    if cell == 0:
                        color = self.gray
                    elif cell == 1:
                        color = self.black
                    elif cell == 2:
                        color = self.red
                    else:
                        color = self.gray

                pygame.draw.rect(self.screen, color, 
                                (col * self.cell_width, row * self.cell_height, 
                                self.cell_width, self.cell_height))

        # Draw gridlines
        for x in range(0, self.screen_width, self.cell_width):
            pygame.draw.line(self.screen, self.black, (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.cell_height):
            pygame.draw.line(self.screen, self.black, (0, y), (self.screen_width, y))

    
    def draw_goal(self):
        pygame.draw.rect(self.screen, self.green, 
                        (self.goal_col * self.cell_width, self.goal_row * self.cell_height, 
                         self.cell_width, self.cell_height))
        
    def agent_start(self):
        return (1, 1)
    
    def is_goal(self, position):
        x, y = position 
        return x == self.goal_col and y == self.goal_row
    
    def draw_q_values(self, q_table):
        font = pygame.font.Font(None, 20)
        
        action_positions = {
            'up': lambda col, row: (col * self.cell_width + self.cell_width // 2 - 10, row * self.cell_height + 2),
            'down': lambda col, row: (col * self.cell_width + self.cell_width // 2 - 10, row * self.cell_height + self.cell_height - 16),
            'left': lambda col, row: (col * self.cell_width + 2, row * self.cell_height + self.cell_height // 2 - 8),
            'right': lambda col, row: (col * self.cell_width + self.cell_width - 30, row * self.cell_height + self.cell_height // 2 - 8),
        }

        for (col, row), actions in q_table.items():
            if not actions:
                continue

            best_action = max(actions, key=actions.get)

            for action, q_val in actions.items():
                pos = action_positions[action](col, row)

                if action == best_action:
                    color = (0, 255, 0)  # Best action: green
                elif q_val < 0:
                    color = (0, 0, 0)  # Negative Q-value: red
                else:
                    color = (200, 200, 200)  # Neutral: gray

                text_surface = font.render(f"{q_val:.1f}", True, color)
                self.screen.blit(text_surface, pos)
    
    def get_next_position(self, position, action):
        x, y = position
        if action == "up":
            y -= 1
        elif action == "down":
            y += 1
        elif action == "left":
            x -= 1
        elif action == "right":
            x += 1
        
        if (0 <= x < self.cols and 0 <= y < self.rows and self.maze[y][x] == 0):
            return (x, y)
        
        return position
    
    def get_reward(self, position):
        if self.is_goal(position):
            return 100
        elif self.maze[position[1]][position[0]] == 0:
            return -1
        elif self.maze[position[1]][position[0]] == 2:
            return -10
        else:
            return -100
