from .constants import SQUARE_SIZE, l1, l2, l3, l4


class Building:
    def __init__(self, build, height):
        self.height = height
        self.row = build[0]
        self.col = build[1]
        self.player = None
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 - 50
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2 - 50

    def get_height(self):
        return self.height

    def draw(self, win):
        if self.height == 1:
            win.blit(l1, (self.x, self.y))
        elif self.height == 2:
            win.blit(l2, (self.x, self.y))
        elif self.height == 3:
            win.blit(l3, (self.x, self.y))
        else:
            win.blit(l4, (self.x, self.y))
