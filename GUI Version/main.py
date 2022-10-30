import pygame

from santorini.menus import Start, Options
from santorini.minimax import minimax
from santorini.game import Game, get_row_col_from_mouse
from santorini.constants import HEIGHT, WIDTH, FPS, player_two, player_one

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True
game_mode = "move"
state = "start"

game = Game(win, "minimax")
start = Start(win)
options = Options(win)

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if game.is_over:
            print("Player {} has won!".format(game.turn))
            run = False

        elif event.type == pygame.QUIT:
            run = False

        elif state == "start":
            pygame.display.set_caption('Start')
            pos = pygame.mouse.get_pos()
            start.update(pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                state = start.get_state(state, pos)

        elif state == "options":
            pygame.display.set_caption('Options')
            pos = pygame.mouse.get_pos()
            options.update(pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                options.get_updates(pos)
                state = options.state
                play_mode = options.game_type

        elif state == "play":
            pygame.display.set_caption('Game')
            if options.game_type == "minimax" and game.turn == player_two:
                move_score, move_board = minimax(game.board, game.board.player_two_heights, 0, 3, float('-inf'),
                                                 float('inf'), player_two, game)

                if move_score >= 1000:
                    game.is_over = True
                elif move_score > 20:
                    game.board = move_board
                else:
                    game.board.best_build(player_two, player_one)

                game.change_turn()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game_mode = game.mode_button.check_mode(pos, game_mode)

                # A very ugly solution but only temporary
                if not game.exit_button.check_mode(pos, "start"):
                    state = "start"  # Redirect to start menu
                    game = Game(win, game_mode)  # Reset game instance

                game.select(row, col)

            game.update(game_mode)
