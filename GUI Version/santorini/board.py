import pygame

from santorini.worker import Worker
from santorini.building import Building
from santorini.constants import SQUARE_SIZE, ROWS, COLS, BROWN, YELLOW


def possible_moves(worker):
    return [(worker.row - 1, worker.col), (worker.row, worker.col - 1), (worker.row + 1, worker.col),
            (worker.row, worker.col + 1), (worker.row - 1, worker.col - 1), (worker.row - 1, worker.col + 1),
            (worker.row + 1, worker.col - 1), (worker.row + 1, worker.col + 1)]


class Board:
    def __init__(self):
        # Will update with user selected starting positions
        self.occupied = [(1, 2), (2, 1), (2, 3), (3, 2)]
        self.buildings = []
        self.board = []
        self.create_board()

    def move(self, worker, row, col):
        updated_index = self.occupied.index((worker.row, worker.col))
        self.occupied[updated_index] = (row, col)

        if (row, col) in self.buildings:  # New location has a building on it
            # Get respective heights before they are modified
            building_height = Building.get_height(self.board[row][col])
            worker_height = worker.height

            # Check if old pos has a building that needs to be replaced
            if (worker.row, worker.col) in self.buildings:
                self.board[row][col] = (Building([worker.row, worker.col], worker_height))

            # Update worker details and remove building from record as it is now occupied
            worker.height = building_height
            worker.on_building = True

        elif worker.on_building:  # Worker Descending
            self.board[row][col] = (Building([worker.row, worker.col], worker.height))  # Replace old building
            # Reset worker details
            worker.on_building = False
            worker.height = 0

        self.board[worker.row][worker.col], self.board[row][col] = self.board[row][col], self.board[worker.row][
            worker.col]
        worker.move(row, col)

    def build(self, row, col):
        if (row, col) in self.buildings:
            height = Building.get_height(self.board[row][col])
            self.board[row][col] = (Building([row, col], height + 1))
        else:
            self.buildings.append((row, col))
            self.board[row][col] = (Building([row, col], 1))

    def get_worker(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)

        self.board[1][2] = (Worker(1, 2, "One"))
        self.board[2][1] = (Worker(2, 1, "One"))
        self.board[2][3] = (Worker(2, 3, "Two"))
        self.board[3][2] = (Worker(3, 2, "Two"))

    def draw(self, win):
        win.fill(BROWN)

        for row in range(ROWS):
            # Draw background
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, YELLOW, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Draw workers
            for col in range(COLS):
                worker = self.board[row][col]
                if worker != 0:
                    worker.draw(win)

    def get_valid_moves(self, worker):
        valid_moves = possible_moves(worker)
        valid_builds = possible_moves(worker)

        valid_moves[:] = [move for move in valid_moves if move not in self.occupied]
        valid_builds[:] = [move for move in valid_builds if move not in self.occupied]

        # print("Worker Level: {}".format(worker.height))

        for move in valid_moves:
            if move in self.buildings:
                building_height = Building.get_height(self.board[move[0]][move[1]])
                # Level is only 1 higher than worker and building is not a dome
                if worker.height + 1 < building_height or building_height == 4:
                    valid_moves.remove(move)

        return valid_moves, valid_builds
