import pygame

FPS = 60
ROWS, COLS = 5, 5
HEIGHT, WIDTH = 600, 600
SQUARE_SIZE = WIDTH // COLS

# Board/Piece colours
BROWN = (184, 134, 74)
YELLOW = (227, 193, 111)

# Worker placeholder
red_worker = pygame.transform.scale(pygame.image.load('assets/red.png'), (100, 100))
yellow_worker = pygame.transform.scale(pygame.image.load('assets/yellow.png'), (100, 100))

# Worker option placeholders
move_icon = pygame.transform.scale(pygame.image.load('assets/move.png'), (50, 50))
build_icon = pygame.transform.scale(pygame.image.load('assets/build.png'), (50, 50))

# Tile placeholders, currently unused
tile_one = pygame.transform.scale(pygame.image.load('assets/tile_one.png'), (100, 100))
tile_two = pygame.transform.scale(pygame.image.load('assets/tile_two.png'), (100, 100))

# Button placeholder
button_icon = pygame.image.load("assets/ugly_button.png")

# Building placeholders
l1 = pygame.transform.scale(pygame.image.load('assets/level_one.png'), (100, 100))
l2 = pygame.transform.scale(pygame.image.load('assets/level_two.png'), (100, 100))
l3 = pygame.transform.scale(pygame.image.load('assets/level_three.png'), (100, 100))
l4 = pygame.transform.scale(pygame.image.load('assets/level_four.png'), (100, 100))
