"""
Contains the game class which is used to manage the mechanics of the game, this is the most import class and must be
updated for each pygame tick
"""
import pygame

from ..components.board import Board
from ..components.button import Button
from ..utils.functions import calc_pos, god_conditions
from ..utils.assets import MOVE_ICON, BUILD_ICON
from ..utils.constants import BUTTON_SIZE_ONE, PLAYER_ONE, PLAYER_TWO, DEFAULT_POSITIONS


class Game:
    """
    Class to manage the mechanics of the game
    """
    def __init__(self, win, starting_positions):
        if starting_positions is None:
            starting_positions = DEFAULT_POSITIONS

        self.state, self.selected, self.last_move = None, None, None
        self.using_gods, self.is_over = False, False
        self.valid_moves, self.valid_builds = [], []
        self.mode = "moving"  # Player either moving or building
        self.turn = PLAYER_ONE  # Current players move
        self.board = Board(starting_positions)
        self.gods = []
        self.win = win
        self.mode_button = Button(550, 20, self.mode, BUTTON_SIZE_ONE)  # Switch between moving and building
        self.confirm_button = Button(300, 20, "confirm", BUTTON_SIZE_ONE)  # Confirm start positions
        self.exit_button = Button(50, 20, "exit", BUTTON_SIZE_ONE)  # Return to start menu

    def select(self, row, col):
        """
        Given a row and column select the relevant worker or position and check if the selection is valid
        :param row: board row
        :param col: board column
        :return: True if valid selection, otherwise False
        """
        result = None

        if self.selected:
            if not self.board.user_select:
                old_heights = [self.board.player_one_heights + self.board.player_two_heights]
                result = self.action(row, col)
                if result:
                    if self.using_gods:
                        new_heights = [self.board.player_one_heights + self.board.player_two_heights]
                        self.update_last_move(old_heights, new_heights, row, col)
                    else:
                        self.change_turn()
            else:
                self.change_start_pos(row, col)

            if not result:
                self.selected = None

        worker = self.board.get_worker(row, col)
        # Ensure valid selection made
        if worker != 0 and worker.player == self.turn:
            self.selected = worker
            # If using gods the valid moves/builds are different
            if self.using_gods:
                self.valid_moves, self.valid_builds = self.board.god_moves(worker, self.current_god(), self.last_move)
            else:
                self.valid_moves, self.valid_builds = self.board.valid_moves(worker)
            return True

        return False

    def update_last_move(self, old_heights, new_heights, row, col):
        """
        When using gods the last move needs to be recorded, this is used to track when to end turns and ensure valid
        moves are correct
        :param old_heights: heights before move
        :param new_heights: heights after move
        :param row:
        :param col:
        """
        if old_heights != new_heights:
            self.last_move = "climbing"
        elif self.last_move is not None:
            if self.last_move[0] == "building":
                self.last_move = "second_build"
            elif self.mode == "building":
                self.last_move = ["building", [row, col]]
        else:
            self.last_move = self.mode

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

            if self.mode == "moving" and [row, col] in self.valid_moves:
                self.board.move(self.selected, row, col)

                # Player has reached winning height
                if self.board.get_worker(row, col).height == 3:
                    self.is_over = True
                return True

            elif self.mode == "building" and [row, col] in self.valid_builds:
                self.board.build(row, col)
                return True

        else:
            return False

    def change_start_pos(self, row, col):
        """
        Update the starting position of a worker
        :param row: selected row
        :param col: selected column
        :return: True if selection is valid
        """
        # Check selected position is not occupied and user is not hovering over the confirm button
        if self.selected and [row, col] not in self.board.occupied and not self.confirm_button.hovered:
            self.board.move(self.selected, row, col)

            return True

    def change_turn(self):
        """
        Switch the turn of the game
        """
        # Reset valid options
        self.valid_moves, self.valid_builds = [], []

        # Switch turn
        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        else:
            self.turn = PLAYER_ONE

    def current_god(self):
        """
        Get current player's god
        :return: god reference
        """
        if self.using_gods and self.gods != []:
            if self.turn == PLAYER_ONE:
                return self.gods[0]
            else:
                return self.gods[1]

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

        self.exit_button.update_colour()
        self.mode_button.update_colour()
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

        # Only shows if user changing starting positions or gods are active
        if self.board.user_select or self.using_gods:
            self.confirm_button.update_colour()
            self.confirm_button.draw(self.win)
            change_turn = self.confirm_button.handle_event(event, "confirm")

            if self.using_gods and self.gods != []:
                god = self.current_god()

                condition = god_conditions(self.last_move, god)

                if condition == "move":
                    self.mode = "moving"
                elif condition in ["upto l2", "new", "build"]:
                    self.mode = "building"

                # Can only continue turn if they do not climb
                if god == "Prometheus" and self.last_move == "climbing":
                    self.change_turn()
                # Only able to build again if built first
                elif god in ["Hephaestus", "Demeter"] and self.last_move in ["moving", "second_build"]:
                    self.change_turn()
                # Unlimited moves until they climb or build
                elif god == "Hermes" and self.last_move in ["climbing", "building"]:
                    self.change_turn()

            if change_turn:
                if self.turn == PLAYER_TWO:
                    self.board.user_select = False
                    self.mode = "moving"

                self.last_move = None
                self.change_turn()

        pygame.display.update()
