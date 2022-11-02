import pygame

from santorini.game import Game
from santorini.menus import Start, Options
from santorini.algorithms.greedy import greedy
from santorini.algorithms.minimax import minimax
from santorini.constants import HEIGHT, WIDTH, FPS, player_two, SQUARE_SIZE


class Santorini:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True
        self.game_mode = "move"
        self.state = "start"
        self.game = Game(self.win, "minimax")
        self.start = Start(self.win)
        self.options = Options(self.win)
        self.score = 0

    def start(self):
        while self.run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if self.game.is_over:
                    print("Player {} has won!".format(self.game.turn))
                    self.run = False

                elif event.type == pygame.QUIT:
                    self.run = False

                elif self.state == "start":
                    pygame.display.set_caption('Start')
                    pos = pygame.mouse.get_pos()
                    self.start.update(pos)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state = self.start.get_state(self.state, pos)

                elif self.state == "options":
                    pygame.display.set_caption('Options')
                    pos = pygame.mouse.get_pos()
                    self.options.update(pos)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.options.get_updates(pos)
                        self.state = self.options.state
                        self.game_mode = self.options.game_type

                elif self.state == "play":
                    pygame.display.set_caption('Game')
                    if self.game.turn == player_two and self.options.game_type != "two":
                        if self.options.game_type == "minimax":
                            move_score, move_board = minimax(self.game.board, 3, float('-inf'), float('inf'), True,
                                                             False, self.game)
                            build_score, build_board = minimax(self.game.board, 3, float('-inf'), float('inf'), True,
                                                               True, self.game)
                            if move_score > build_score:
                                print("\nMoving")
                                print("Final Score: {}".format(move_score))
                                print("Best positions: {}".format(move_board.occupied))
                                self.game.board = move_board
                                self.game.change_turn()
                            else:
                                print("\nBuilding")
                                print("Final Score: {}".format(build_score))
                                print("Best positions: {}".format(build_board.occupied))
                                self.game.board = build_board

                        else:
                            # Currently has no win confirmation
                            self.game.board = greedy(self.game, player_two)

                        self.game.change_turn()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        self.game.mode = self.game.mode_button.check_mode(pos, self.game.mode)

                        # A very ugly solution but hopefully only temporary
                        if not self.game.exit_button.check_mode(pos, "start"):
                            self.state = "start"  # Redirect to start menu
                            self.game = Game(self.win, self.game.mode)  # Reset self.game.instance

                        self.game.select(row, col)

                    self.game.update(self.game.mode)


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


if __name__ == "__main__":
    game = Santorini()
    Santorini.start(game)
