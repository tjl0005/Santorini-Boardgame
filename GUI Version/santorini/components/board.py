"""
Contains the board class to be used for creating the board, displaying the board and handling moving and building
"""
import pygame

from ..components.worker import Worker
from ..components.building import Building
from ..utils.constants import SQUARE_SIZE, ROWS, COLS, PLAYER_ONE, PLAYER_TWO, DARK_GREEN, LIGHT_GREEN, GREEN


class Board:
    """
    Class used to generate the board and track occupied spaces and worker heights
    """
    def __init__(self, starting_positions):
        # Will update with user selected starting positions
        self.occupied = [(1, 2), (2, 1), (2, 3), (3, 2)]  # Represents worker locations
        # Track heights of each player's workers
        self.player_one_heights = [0, 0]
        self.player_two_heights = [0, 0]
        self.starting_positions = starting_positions
        self.buildings = []
        self.board = []
        self.create_board()

    def create_board(self):
        """
        Generate the initial board to be used
        """
        # Initialise board
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)

        # Initialise worker positions
        worker_one = self.starting_positions[0]
        worker_two = self.starting_positions[1]
        worker_three = self.starting_positions[2]
        worker_four = self.starting_positions[3]
        # Place workers on board
        self.board[worker_one[0]][worker_one[1]] = (Worker(worker_one, PLAYER_ONE, 0))
        self.board[worker_two[0]][worker_two[1]] = (Worker(worker_two, PLAYER_ONE, 1))
        self.board[worker_three[0]][worker_three[1]] = (Worker(worker_three, PLAYER_TWO, 0))
        self.board[worker_four[0]][worker_four[1]] = (Worker(worker_four, PLAYER_TWO, 1))

    def draw(self, win):
        """
        Display the board in its current state, including all pieces present
        :param win:
        """
        win.fill(LIGHT_GREEN)
        for row in range(ROWS):
            # Draw tiles
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, DARK_GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                item = self.board[row][col]  # Refers to either a worker or a building
                if item != 0:
                    item.draw(win)

    def possible_moves(self, worker):
        """
        Calculate all possible moves for a worker, removing any moves where a worker is present
        :param worker: the worker whose reach is being obtained
        :return:
        """
        moves = [(worker.row - 1, worker.col), (worker.row, worker.col - 1), (worker.row + 1, worker.col),
                 (worker.row, worker.col + 1), (worker.row - 1, worker.col - 1), (worker.row - 1, worker.col + 1),
                 (worker.row + 1, worker.col - 1), (worker.row + 1, worker.col + 1)]

        # Remove any moves where a worker is
        moves[:] = [move for move in moves if move not in self.occupied]

        return moves

    def get_valid_moves(self, worker):
        """
        Get all moves for a worker that can be made, meaning each new position does not have a building that is too high
        for a worker or a dome. As well as removing domes from valid builds.
        :param worker: the worker whose reaches are being obtained
        :return: valid moves and builds that are possible for a worker
        """
        valid_moves = self.possible_moves(worker)  # Worker can move to these position
        valid_builds = self.possible_moves(worker)  # Worker can build on these positions

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
        """
        Given a worker update their position on the board to the given row and column
        :param worker: worker to move
        :param row: desired row
        :param col: desired column
        """
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

        # Update player height tracker
        if worker.player == PLAYER_ONE:
            self.player_one_heights[worker.index] = worker.height
        else:
            self.player_two_heights[worker.index] = worker.height

        # Update board
        self.board[worker.row][worker.col], self.board[row][col] = self.board[row][col], self.board[worker.row][
            worker.col]
        worker.move(row, col)

    def build(self, row, col):
        """
        Given a row and column either add a new building or build upon an existing building
        :param row:
        :param col:
        """
        # Building on an existing building
        if (row, col) in self.buildings:
            height = self.board[row][col].height
            # Increase height
            self.board[row][col] = (Building([row, col], height + 1))
        # Producing new building on board
        else:
            self.buildings.append((row, col))
            self.board[row][col] = (Building([row, col], 1))

    def get_worker(self, row, col):
        """
        Given a row and column return the present worker
        :param row: desired row
        :param col: desired column
        :return: the contents of the given location on the board
        """
        return self.board[row][col]

    def get_player_workers(self, player):
        """
        Given a player (e.g. player_one) return all of their workers
        :param player:
        :return: workers for a given player
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.player == player:
                    pieces.append(piece)
        return pieces
