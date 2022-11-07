"""
Contains the class used to generate buildings
"""
from ..utils.functions import calc_pos
from ..utils.assets import L1, L2, L3, L4


class Building:
    """
    Class representing a building on the board
    """
    def __init__(self, build, height):
        self.height = height
        self.player = None
        self.row = build[0]
        self.col = build[1]
        self.x = 0
        self.y = 0
        self.x, self.y = calc_pos(self.col, self.row, 50)

    def draw(self, win):
        """
        Place relevant building asset on board
        :param win: pygame window
        """
        if self.height == 1:
            win.blit(L1, (self.x, self.y))
        elif self.height == 2:
            win.blit(L2, (self.x, self.y))
        elif self.height == 3:
            win.blit(L3, (self.x, self.y))
        else:
            win.blit(L4, (self.x, self.y))
