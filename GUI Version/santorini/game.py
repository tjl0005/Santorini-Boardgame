import pygame

from santorini.button import Button
from santorini.board import Board
from santorini.worker import Worker
from santorini.constants import SQUARE_SIZE, move_icon, build_icon


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
    def __init__(self, win):
        self.mode = "move"
        self.selected = None
        self.turn = "One"
        self.valid_moves = {}
        self.valid_builds = {}
        self.mode_button = Button(550, 20, "Mode")
        self.board = Board()
        self.is_over = False
        self.win = win

    def update(self, mode):
        self.board.draw(self.win)
        if self.mode == "move":
            self.draw_valid_moves(self.valid_moves, move_icon)
        else:
            self.draw_valid_moves(self.valid_builds, build_icon)

        self.mode_button.update(self.win)
        self.mode_button.change_colour(pygame.mouse.get_pos())
        self.mode = mode
        pygame.display.update()

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

    def draw_valid_moves(self, moves, icon):
        for move in moves:
            row, col = move
            x, y = calc_pos(col, row)
            self.win.blit(icon, (x, y))

    def change_turn(self):
        # Opposite of current
        self.valid_moves = {}
        self.valid_builds = {}
        if self.turn == "One":
            self.turn = "Two"
        else:
            self.turn = "One"
