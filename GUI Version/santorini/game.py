"""
To write
"""
import pygame

from .components.board import Board
from .components.button import Button
from .utils.functions import calc_pos
from .utils.assets import MOVE_ICON, BUILD_ICON
from .utils.constants import BUTTON_SIZE_ONE, PLAYER_ONE, PLAYER_TWO, DEFAULT_POSITIONS


class Game:
    """
    Class to manage the mechanics of the game
    """
    def __init__(self, win, starting_positions):
        if starting_positions is None:
            starting_positions = DEFAULT_POSITIONS

        self.mode = "moving"  # Player either moving or building
        self.mode_button = Button(550, 20, self.mode, BUTTON_SIZE_ONE)  # Switch between moving and building
        self.exit_button = Button(50, 20, "exit", BUTTON_SIZE_ONE)  # Return to start menu
        self.selected = None  # Selected worker
        self.turn = PLAYER_ONE  # Current players move
        self.valid_moves = {}
        self.valid_builds = {}
        self.board = Board(starting_positions)
        self.is_over = False
        self.state = None
        self.win = win

    def select(self, row, col):
        """
        Given a row and column select the relevant worker or position and check if the selection is valid
        :param row: board row
        :param col: board column
        :return: True if valid selection, otherwise False
        """
        if self.selected:
            result = self.action(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        worker = self.board.get_worker(row, col)
        # Ensure valid selection made
        if worker != 0 and worker.player == self.turn:
            self.selected = worker
            self.valid_moves, self.valid_builds = self.board.get_valid_moves(worker)
            return True

        return False

    def draw_valid_moves(self, moves, icon):
        """
        Draw possible worker moves on the screen with the relevant icon
        :param moves: valid moves
        :param icon: move type icon (Move or Build)
        """
        for move in moves:
            row, col = move
            x, y = calc_pos(col, row, 25)
            self.win.blit(icon, (x, y))

    def action(self, row, col):
        """
        Perform action of moving a player or building on the board, changing the turn and detecting a win
        :param row: board row
        :param col: board column
        :return: True if action performed, otherwise False
        """
        if self.selected:
            if self.mode == "moving" and (row, col) in self.valid_moves:
                self.board.move(self.selected, row, col)

                # Player has reached winning height
                if self.board.get_worker(row, col).height == 3:
                    self.is_over = True

                self.change_turn()

            elif self.mode == "building" and (row, col) in self.valid_builds:
                self.board.build(row, col)
                self.change_turn()

        else:
            return False

        return True

    def change_turn(self):
        """
        Switch the turn of the game
        """
        # Reset valid options
        self.valid_moves = {}
        self.valid_builds = {}
        # Switch turn
        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        else:
            self.turn = PLAYER_ONE

    def update(self, event):
        """
        Update board contents, used mainly for buttons and detecting game_mode
        :param event: pygame event
        """
        self.board.draw(self.win)  # Display board
        self.mode_button.update_text(self.mode)  # Change button text so correct mode shown to user
        # Show relevant moves
        if self.mode == "moving":
            self.draw_valid_moves(self.valid_moves, MOVE_ICON)
        else:
            self.draw_valid_moves(self.valid_builds, BUILD_ICON)

        self.exit_button.update()
        self.mode_button.update()

        self.exit_button.draw(self.win)
        self.mode_button.draw(self.win)

        mode = self.mode_button.handle_event(event, "mode")
        state = self.exit_button.handle_event(event, "mode")

        if mode:  # Update mode
            self.mode = mode
        elif state == "start":  # Return to start screen
            self.state = "start"
        else:  # No change required
            self.state = None

        pygame.display.update()
