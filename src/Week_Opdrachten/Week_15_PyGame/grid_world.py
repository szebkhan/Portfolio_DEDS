import pygame

class GridWorld:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("2D Grid Game")
        
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
        
        self.maze = [
            [0, 1, 0, 0, 0, 1, 0, 0, 2, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 2, 0, 1, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 2, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 2],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
        ]

        
        # Goal position
        self.goal_row = 9
        self.goal_col = 9
    
    def draw_maze(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]
                if cell == 0:
                    color = self.gray  # free space
                elif cell == 1:
                    color = self.black  # walls
                elif cell == 2:
                    color = self.red    # obstacles
                else:
                    color = self.gray  # default fallback

                pygame.draw.rect(self.screen, color, 
                                (col * self.cell_width, row * self.cell_height, 
                                self.cell_width, self.cell_height))
        
        # Teken gridlines
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
    
    def draw_q_values_simple(self, q_table):
        font = pygame.font.Font(None, 20)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == 0:
                    state = (col, row)
                    if state in q_table:
                        max_q = max(q_table[state].values())
                        text = font.render(f"{max_q:.1f}", True, (255, 255, 255))
                        self.screen.blit(text, (col * self.cell_width + 5, row * self.cell_height + 5))
    
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
        else:
            return -100
