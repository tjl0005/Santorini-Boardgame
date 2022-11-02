import pygame

from .constants import SQUARE_SIZE, ROWS, COLS, BROWN, YELLOW, player_one, player_two
from .components.building import Building
from .components.worker import Worker


class Board:
    def __init__(self):
        # Will update with user selected starting positions
        self.occupied = [(1, 2), (2, 1), (2, 3), (3, 2)]
        self.player_one_heights = [0, 0]
        self.player_two_heights = [0, 0]
        self.buildings = []
        self.board = []
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)

        self.board[1][2] = (Worker(1, 2, player_one, 0))
        self.board[2][1] = (Worker(2, 1, player_one, 1))
        self.board[2][3] = (Worker(2, 3, player_two, 0))
        self.board[3][2] = (Worker(3, 2, player_two, 1))

    def draw(self, win):
        win.fill(BROWN)

        for row in range(ROWS):
            # Draw background
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, YELLOW, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Currently need separate loops due to background squares being drawn over workers
        for row in range(ROWS):
            # Draw workers
            for col in range(COLS):
                item = self.board[row][col]  # Refers to either a worker or a building
                if item != 0:
                    item.draw(win)

    def possible_moves(self, worker):
        moves = [(worker.row - 1, worker.col), (worker.row, worker.col - 1), (worker.row + 1, worker.col),
                 (worker.row, worker.col + 1), (worker.row - 1, worker.col - 1), (worker.row - 1, worker.col + 1),
                 (worker.row + 1, worker.col - 1), (worker.row + 1, worker.col + 1)]

        moves[:] = [move for move in moves if move not in self.occupied]

        return moves

    def get_valid_moves(self, worker):
        valid_moves = self.possible_moves(worker)
        valid_builds = self.possible_moves(worker)

        for move in valid_moves:
            if move in self.buildings:
                building_height = self.board[move[0]][move[1]].height
                # Level is only 1 higher than worker and building is not a dome
                if worker.height + 1 < building_height or building_height > 3:
                    valid_moves.remove(move)
                if building_height > 3:
                    valid_builds.remove(move)

        return valid_moves, valid_builds

    def move(self, worker, row, col):
        updated_index = self.occupied.index((worker.row, worker.col))
        self.occupied[updated_index] = (row, col)

        if (row, col) in self.buildings:  # New location has a building on it
            # Get respective heights before they are modified
            building_height = self.board[row][col].height
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

        if worker.player == player_one:
            self.player_one_heights[worker.index] = worker.height
        else:
            self.player_two_heights[worker.index] = worker.height

        self.board[worker.row][worker.col], self.board[row][col] = self.board[row][col], self.board[worker.row][
            worker.col]
        worker.move(row, col)

    def build(self, row, col):
        if (row, col) in self.buildings:
            height = self.board[row][col].height
            self.board[row][col] = (Building([row, col], height + 1))
        else:
            self.buildings.append((row, col))
            self.board[row][col] = (Building([row, col], 1))

    def get_worker(self, row, col):
        return self.board[row][col]

    def get_player_workers(self, player):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.player == player:
                    pieces.append(piece)
        return pieces
