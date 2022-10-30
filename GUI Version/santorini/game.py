import pygame
from .board import Board
from .button import Button
from .constants import SQUARE_SIZE, move_icon, build_icon, button_size_one, player_one, player_two


def calc_pos(col, row):
    x = SQUARE_SIZE * col + SQUARE_SIZE // 2 - 25
    y = SQUARE_SIZE * row + SQUARE_SIZE // 2 - 25

    return x, y


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


class Game:
    def __init__(self, win, game_type):
        self.game_type = game_type
        self.mode = "move"
        self.mode_button = Button(550, 20, "Mode", button_size_one)
        self.exit_button = Button(50, 20, "Exit", button_size_one)
        self.selected = None
        self.turn = player_one
        self.valid_moves = {}
        self.valid_builds = {}
        self.board = Board()
        self.is_over = False
        self.win = win

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        worker = self.board.get_worker(row, col)
        if worker != 0 and worker.player == self.turn:
            self.selected = worker
            self.valid_moves, self.valid_builds = self.board.get_valid_moves(worker)
            return True

        return False

    def draw_valid_moves(self, moves, icon):
        for move in moves:
            row, col = move
            x, y = calc_pos(col, row)
            self.win.blit(icon, (x, y))

    def _move(self, row, col):
        if self.selected:
            if self.mode == "move" and (row, col) in self.valid_moves:
                self.board.move(self.selected, row, col)

                if self.board.get_worker(row, col).height == 3:
                    self.is_over = True

                self.change_turn()

            elif self.mode == "build" and (row, col) in self.valid_builds:
                self.board.build(row, col)
                self.change_turn()

        else:
            return False

        return True

    def change_turn(self):
        # Opposite of current
        self.valid_moves = {}
        self.valid_builds = {}
        if self.turn == player_one:
            self.turn = player_two
        else:
            self.turn = player_one

    def update(self, mode):
        self.board.draw(self.win)
        self.mode = mode

        if self.mode == "move":
            self.draw_valid_moves(self.valid_moves, move_icon)
        else:
            self.draw_valid_moves(self.valid_builds, build_icon)

        pos = pygame.mouse.get_pos()

        self.exit_button.update(self.win)
        self.exit_button.change_colour(pos)
        self.mode_button.update(self.win)
        self.mode_button.change_colour(pos)
        pygame.display.update()
