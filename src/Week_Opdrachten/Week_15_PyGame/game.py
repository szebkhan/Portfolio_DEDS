import pygame
import random
import sys

#Initializeer game
pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Too Dee Game")

# Maze layout
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Grid rijen en kolommen 
rows = 15
cols = 15

# Gebruikte kleuren
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)

# Grid blok groottes
cell_width = screen_width // cols
cell_height = screen_height // rows

#Coördinaten voor user-controlled blok
x = 1
y = 1

# Maze en gridlines tekenen in game window
def draw_maze():
    for row in range(rows):
        for col in range(cols):
            color = white if maze[row][col] == 0 else red
            pygame.draw.rect(screen, color, (col * cell_width, row * cell_height, cell_width, cell_height))
    for x in range(0, screen_width, cell_width):
        pygame.draw.line(screen, black, (x, 0), (x, screen_height))
    for y in range(0, screen_height, cell_height):
        pygame.draw.line(screen, black, (0, y), (screen_width, y))

# Game beginnen wanneer code wordt ge-execute
running = True
while running:
    pygame.time.delay(100)

    screen.fill(white)
    draw_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Game controls: W = Up, A = Left, S = Down, D = Right
    if keys[pygame.K_a] and x > 0 and maze[y][x - 1] == 0:
        x -= 1
    
    if keys[pygame.K_d] and x < cols - 1 and maze[y][x + 1] == 0:
        x += 1

    if keys[pygame.K_w] and y > 0 and maze[y - 1][x] == 0:
        y -= 1

    if keys[pygame.K_s] and y < rows - 1 and maze[y + 1][x] == 0:
        y += 1

    # Maak user-controlled gridblok
    pygame.draw.rect(screen, blue, (x * cell_width, y * cell_height, cell_width, cell_height))

    goal_row = 13
    goal_col = 13

    # Maak goal voor maze
    pygame.draw.rect(screen, green, (goal_col * cell_width, goal_row * cell_height, cell_width, cell_height))

    if x == goal_row and y == goal_col:
        print ("gewonnen")
        running = False

    # Update de game window
    pygame.display.update()

# Quit de game als while loop stopt
pygame.quit()