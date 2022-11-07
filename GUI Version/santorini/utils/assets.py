"""
Assets used throughout the project
"""
import pygame

pygame.init()

# Font
SQUIRK = "assets/Squirk.ttf"
TITLE_FONT = pygame.font.Font(SQUIRK, 48)
MESSAGE_FONT = pygame.font.Font(SQUIRK, 40)

# Menu Items
GAME_ICON = pygame.image.load("assets/icon.png")
CLOUD = pygame.transform.scale(pygame.image.load('assets/cloud.png'), (350, 100))
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load('assets/background.png'), (600, 600))
SUPPORTER = pygame.transform.scale(pygame.image.load('assets/woo.png'), (200, 200))
GRASS = pygame.transform.scale(pygame.image.load('assets/grass_tile.png'), (120, 120))

# Worker placeholder
RED_WORKER = pygame.transform.scale(pygame.image.load('assets/red.png'), (100, 100))
YELLOW_WORKER = pygame.transform.scale(pygame.image.load('assets/yellow.png'), (100, 100))

# Worker option placeholders
MOVE_ICON = pygame.transform.scale(pygame.image.load('assets/move.png'), (50, 50))
BUILD_ICON = pygame.transform.scale(pygame.image.load('assets/build.png'), (50, 50))

# Button placeholder
BUTTON_ICON = pygame.image.load("assets/ugly_button.png")

# Building placeholders
L1 = pygame.transform.scale(pygame.image.load('assets/level_one.png'), (100, 100))
L2 = pygame.transform.scale(pygame.image.load('assets/level_two.png'), (100, 100))
L3 = pygame.transform.scale(pygame.image.load('assets/level_three.png'), (100, 100))
L4 = pygame.transform.scale(pygame.image.load('assets/level_four.png'), (100, 100))
