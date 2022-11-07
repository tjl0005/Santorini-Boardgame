"""
Contains the worker class to be used when handling a player worker
"""
import pygame

from ..utils.functions import calc_pos
from ..utils.constants import PLAYER_ONE, BLUE
from ..utils.assets import RED_WORKER, YELLOW_WORKER, SQUIRK

pygame.init()
font = pygame.font.Font(SQUIRK, 48)


class Worker:
    """
    Class representing the player workers
    """
    def __init__(self, pos, player, index):
        self.player = player
        self.index = index  # Either 0 (First) or 1 (Second) worker of player
        self.on_building = False
        self.height = 0
        self.row = pos[0]
        self.col = pos[1]
        self.x = 0
        self.y = 0
        self.x, self.y = calc_pos(self.col, self.row, 50)

    def move(self, row, col):
        """
        Update worker row, column, x and y coordinates
        :param col: board column
        :param row: board row
        """
        self.row = row
        self.col = col
        self.x, self.y = calc_pos(self.col, self.row, 50)

    def draw(self, win):
        """
        Display worker on board
        :param win: pygame window
        """
        # Place relevant icon
        if self.player == PLAYER_ONE:
            win.blit(RED_WORKER, (self.x, self.y))
        else:
            win.blit(YELLOW_WORKER, (self.x, self.y))

        if self.on_building:
            text = font.render(str(self.height), True, BLUE)
            text_rect = text.get_rect()
            win.blit(text, text_rect)
