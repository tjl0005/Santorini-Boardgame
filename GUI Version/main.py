"""
Main file of the graphical version of Santorini
"""
import pygame

from santorini.game import Game
from santorini.utils.assets import GAME_ICON
from santorini.algorithms import greedy, minimax
from santorini.menus import Start, Options, Winner, Select
from santorini.utils.functions import get_row_col_from_mouse
from santorini.utils.constants import HEIGHT, WIDTH, FPS, PLAYER_TWO


class Santorini:
    """
    Used to start playing the game
    """
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True
        self.starting_positions = None  # Initialised in start function
        self.state = "start"  # First screen to be displayed
        # Different screens to be used
        self.game = Game(self.window, self.starting_positions)
        self.start = Start(self.window)
        self.options = Options(self.window)
        self.win_screen = Winner(self.window)
        self.select_pos = Select(self.window)

    def start(self):
        """
        Call to run game
        """
        pygame.display.set_icon(GAME_ICON)
        pygame.display.set_caption('Santorini')

        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                elif self.state == "start":
                    self.game = Game(self.window, self.starting_positions)
                    new_state = self.start.update(event)
                    # Detect if user switching to options menu or starting game
                    if new_state:
                        self.state = new_state

                elif self.state == "select":
                    # Not implemented
                    # self.starting_positions = [[2, 3], [3, 2], [1, 2], [2, 1]]
                    self.select_pos.update(event)
                    self.state = self.select_pos.state

                elif self.state == "options":
                    self.options.update(event)
                    self.state = self.options.state

                elif self.game.is_over or self.state == "win_screen":
                    self.win_screen.update(event, self.game.turn)
                    self.state = self.win_screen.state

                elif self.state == "play":
                    # Algorithm always uses player two
                    if self.game.turn == PLAYER_TWO and self.options.game_type != "Two Player":
                        if self.options.game_type == "Minimax":
                            # Evaluating both moving and building
                            move_score, move_board = minimax.play(self.game.board, 3, float('-inf'),
                                                                  float('inf'), True, False, self.game)
                            build_score, build_board = minimax.play(self.game.board, 3, float('-inf'),
                                                                    float('inf'), True, True, self.game)
                            # Update the current board with the higher scoring minimax board
                            if move_score > build_score:
                                self.game.board = move_board
                            else:
                                self.game.board = build_board

                        else:
                            game_over, greedy_board = greedy.play(self.game, PLAYER_TWO)
                            self.game.board = greedy_board

                        # Ensuring game has not finished
                        if not self.game.is_over:
                            self.game.change_turn()

                    # Enable user worker selection
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        self.game.select(row, col)

                    self.game.update(event)

                    if self.game.state == "start":
                        self.state = "start"  # Redirect to start menu


if __name__ == "__main__":
    game = Santorini()
    Santorini.start(game)
