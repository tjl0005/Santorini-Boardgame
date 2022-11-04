import pygame

from santorini.game import Game
from santorini.menus import Start, Options
from santorini.algorithms.greedy import greedy
from santorini.algorithms.minimax import minimax
from santorini.constants import HEIGHT, WIDTH, FPS, SQUARE_SIZE, player_two, icon, default_positions


class Santorini:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True
        self.state = "start"
        self.game = None
        self.starting_positions = default_positions
        self.start = Start(self.win)
        self.options = Options(self.win)

    def start(self):
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Santorini')

        while self.run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if self.state == "start":
                    self.game = Game(self.win, self.starting_positions)
                    new_state = self.start.update(event)
                    if new_state:
                        self.state = new_state
                    if self.options.start_select == "User Positions":
                        # Currently only switches starting positions of players -> Will update to be user selected
                        self.starting_positions = [[2, 3], [3, 2], [1, 2], [2, 1]]
                    else:
                        self.starting_positions = default_positions

                if self.game.is_over or event.type == pygame.QUIT:
                    print("Player {} has won!".format(self.game.turn))
                    self.run = False

                elif self.state == "options":
                    self.options.update(event)
                    self.state = self.options.state

                elif self.state == "play":
                    if self.game.turn == player_two and self.options.game_type != "Two Player":
                        if self.options.game_type == "Minimax":
                            move_score, move_board = minimax(self.game.board, 3, float('-inf'), float('inf'), True,
                                                             False, self.game)
                            build_score, build_board = minimax(self.game.board, 3, float('-inf'), float('inf'), True,
                                                               True, self.game)
                            if move_score > build_score:
                                print("\nMoving")
                                print("Final Score: {}".format(move_score))
                                print("Best positions: {}".format(move_board.occupied))
                                self.game.board = move_board
                            else:
                                print("\nBuilding")
                                print("Final Score: {}".format(build_score))
                                print("Best positions: {}".format(build_board.occupied))
                                self.game.board = build_board

                        else:
                            # Currently has no win confirmation
                            self.game.board = greedy(self.game.board, player_two)

                        self.game.change_turn()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        self.game.select(row, col)

                    self.game.update(event)

                    if self.game.state == "start":
                        self.state = "start"  # Redirect to start menu


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


if __name__ == "__main__":
    game = Santorini()
    Santorini.start(game)
