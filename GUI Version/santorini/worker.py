from santorini.constants import SQUARE_SIZE, red_worker, yellow_worker


class Worker:
    def __init__(self, row, col, player):
        self.on_building = False
        self.height = 0
        self.row = row
        self.col = col
        self.player = player
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 - 50
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2 - 50

    def get_height(self):
        return self.height

    def draw(self, win):
        if self.player == "One":
            win.blit(red_worker, (self.x, self.y))
        else:
            win.blit(yellow_worker, (self.x, self.y))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
