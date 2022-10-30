from .constants import SQUARE_SIZE, red_worker, yellow_worker, player_one


class Worker:
    def __init__(self, row, col, player, index):
        self.player = player
        self.index = index
        self.on_building = False
        self.height = 0
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 - 50
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2 - 50

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win):
        if self.player == player_one:
            win.blit(red_worker, (self.x, self.y))
        else:
            win.blit(yellow_worker, (self.x, self.y))

    def get_height(self):
        return self.height
