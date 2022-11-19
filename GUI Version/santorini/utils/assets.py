"""
Assets used throughout the project
"""
import pygame

pygame.init()

# Font to be used
SQUIRK = "assets/Squirk.ttf"
# Initialising font usages
TITLE_FONT = pygame.font.Font(SQUIRK, 48)
BUTTON_FONT = pygame.font.Font(SQUIRK, 20)
MESSAGE_FONT = pygame.font.Font(SQUIRK, 40)
OUTLINE_FONT = pygame.font.Font(SQUIRK, 21)
DESCRIPTION_FONT = pygame.font.Font(SQUIRK, 20)

# Menu Items
CLOUD = pygame.image.load('assets/cloud.png')
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load('assets/menu_background.png'), (600, 600))
GAME_BACKGROUND = pygame.image.load('assets/game_background.png')
SUPPORTER = pygame.image.load('assets/woo.png')

# Worker placeholders
RED_WORKER = pygame.transform.scale(pygame.image.load('assets/red.png'), (50, 50))
YELLOW_WORKER = pygame.transform.scale(pygame.image.load('assets/yellow.png'), (50, 50))

# Worker option placeholders
MOVE_ICON = pygame.transform.scale(pygame.image.load('assets/move.png'), (50, 50))
BUILD_ICON = pygame.transform.scale(pygame.image.load('assets/build.png'), (50, 50))

# Button placeholder
BUTTON_ICON = pygame.image.load("assets/the_button_that_survived.png")

# Building placeholders
L1 = pygame.image.load('assets/l1.png')
L2 = pygame.image.load('assets/l2.png')
L3 = pygame.image.load('assets/l3.png')
L4 = pygame.image.load('assets/l4.png')
