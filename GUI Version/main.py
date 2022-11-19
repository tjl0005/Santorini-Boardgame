"""
Main file of the graphical version of Santorini
"""
import pygame

from santorini.screens.game import Game
from santorini.utils.assets import BUILD_ICON
from santorini.algorithms import greedy, minimax
from santorini.screens.menus import Start, Options, Winner, Gods
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
        self.state = "start"  # First screen to be displayed
        self.user_select = False

        # Different screens to be used
        self.game = Game(self.window, self.user_select)
        self.start = Start(self.window)
        self.options = Options(self.window)
        self.gods = Gods(self.window)
        self.winner = Winner(self.window)

    def start(self):
        """
        Call to run game
        """
        pygame.display.set_icon(BUILD_ICON)
        pygame.display.set_caption('Santorini')

        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                elif self.state == "start":
                    self.game = Game(self.window, self.user_select)
                    new_state = self.start.update(event)
                    # Detect if user switching to options menu or starting game
                    if new_state:
                        self.state = new_state

                elif self.state == "options":
                    self.options.update(event)
                    self.state = self.options.state
                    self.user_select = self.options.start_select

                elif self.state == "gods":
                    self.gods.update(event)
                    self.state = self.gods.state

                elif self.game.is_over or self.state == "win_screen":
                    self.winner.update(event, self.game.turn)
                    self.state = self.winner.state

                elif self.state == "play":
                    if self.gods.mode == "Simple Gods":
                        self.game.using_gods = True
                        self.game.gods = [self.gods.player_one_god, self.gods.player_two_god]
                    elif self.gods.mode == "None":
                        self.game.using_gods = False
                        self.game.gods = []
                    else:
                        self.game.using_gods = True
                        self.game.gods = []

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
