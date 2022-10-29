import pygame

from santorini.constants import HEIGHT, WIDTH, FPS
from santorini.game import Game, get_row_col_from_mouse

# TODO: Starting position selection
# TODO: Main selection screen

pygame.display.set_caption('Santorini')
win = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
game = Game(win)
mode = "move"
run = True

while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.is_over:
            print("Player {} has won!".format(game.turn))
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            game.select(row, col)
            mode = game.mode_button.check_input(pos, mode)

        game.update(mode)

pygame.quit()
