import pygame
pygame.font.init()
pygame.display.init()

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
BLUE_2 = (81, 145, 228)
DARK_BLUE_2 = (44, 67, 208)
PURPLE = (17, 104, 217)

# Window Dimensions
WINDOW_INFO = pygame.display.Info()
WIDTH, HEIGHT = WINDOW_INFO.current_w - 450, WINDOW_INFO.current_h - 150
HEADER_HEIGHT = 200

# Maze
CELL_SIZE = 30

REMAINDER_W = WIDTH % CELL_SIZE
if REMAINDER_W == 0:
    REMAINDER_W = CELL_SIZE

REMAINDER_H = (HEIGHT - HEADER_HEIGHT) % CELL_SIZE
if REMAINDER_H == 0:
    REMAINDER_H = CELL_SIZE // 2

MAZE_WIDTH = WIDTH - REMAINDER_W
MAZE_HEIGHT = HEIGHT - HEADER_HEIGHT - REMAINDER_H

# Framerate
FPS = 60
CLOCK = pygame.time.Clock()

# Images and fonts
WEIGHT = pygame.image.load("assets/images/weight.png")
START = pygame.image.load("assets/images/triangle.png")
GOAL = pygame.image.load("assets/images/circle.png")
FONT_14 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 14)
FONT_18 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 18)
