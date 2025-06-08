import pygame

class Agent:
    def __init__(self, start_x, start_y, grid_world):
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.grid_world = grid_world
    
    def move_agent(self, direction): # Beweeg de agent in een bepaalde richting
        if direction == "left" and self.x > 0 and self.grid_world.maze[self.y][self.x - 1] in [0, 2]:
            self.x -= 1
        elif direction == "right" and self.x < self.grid_world.cols - 1 and self.grid_world.maze[self.y][self.x + 1] in [0, 2]:
            self.x += 1
        elif direction == "up" and self.y > 0 and self.grid_world.maze[self.y - 1][self.x] in [0, 2]:
            self.y -= 1
        elif direction == "down" and self.y < self.grid_world.rows - 1 and self.grid_world.maze[self.y + 1][self.x] in [0, 2]:
            self.y += 1
    
    def is_valid_move(self, position): # Check of een positie geldig is (binnen grenzen en geen obstakel)
        x, y = position
        if (0 <= x < self.grid_world.cols and 
            0 <= y < self.grid_world.rows and 
            self.grid_world.maze[y][x] == 0):
            return True
        return False
    
    def reset_position(self): # Reset agent naar startpositie
        self.x = self.start_x
        self.y = self.start_y
    
    def draw_agent(self): # Teken de agent (blauwe vierkant)
        pygame.draw.rect(self.grid_world.screen, self.grid_world.blue, 
                        (self.x * self.grid_world.cell_width, self.y * self.grid_world.cell_height, 
                         self.grid_world.cell_width, self.grid_world.cell_height))
    
    def has_reached_goal(self): # Check of agent het doel heeft bereikt
        return self.x == self.grid_world.goal_col and self.y == self.grid_world.goal_row