import pygame
pygame.font.init()

# Colors
BLACK = (0, 0, 0)
DARK = (11, 53, 71)
GREEN = (26, 188, 157)
GREEN_2 = (104, 224, 185)
BLUE = (100, 206, 228)
WHITE = (255, 255, 255)
YELLOW = (255, 254, 106)
GRAY = (166, 222, 255)
DARK_BLUE = (52, 73, 94)
PURPLE = (82, 123, 201)

# Window Dimensions
WIDTH, HEIGHT = 1230, 900
HEADER_HEIGHT = 200

# Maze
CELL_SIZE = 30
MAZE_WIDTH = WIDTH - CELL_SIZE
MAZE_HEIGHT = HEIGHT - HEADER_HEIGHT

# Framerate
FPS = 60
CLOCK = pygame.time.Clock()

# Images and fonts
WEIGHT = pygame.image.load("assets/images/weight.png")
START = pygame.image.load("assets/images/triangle.png")
GOAL = pygame.image.load("assets/images/circle.png")
FONT_14 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 14)
FONT_18 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 18)
