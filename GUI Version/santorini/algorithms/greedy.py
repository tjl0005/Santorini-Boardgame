"""
An implementation of a greedy algorithm
"""
from ..utils.constants import PLAYER_ONE, PLAYER_TWO


def play(game, player):
    """
    Given a player and game state use a greedy approach to find the best move or build for the player
    :param game:  current game state
    :param player: desired player
    :return: the updated board
    """
    if player == PLAYER_TWO:
        enemy = PLAYER_ONE
    else:
        enemy = PLAYER_TWO

    board = game.board

    # Get all worker details and store as current players and enemies
    workers = board.get_player_workers(PLAYER_TWO)
    worker_reaches = [board.valid_moves(workers[0])[1], board.valid_moves(workers[1])[1]]
    enemies = board.get_player_workers(enemy)
    enemy_reaches = [board.valid_moves(enemies[0])[1] + board.valid_moves(enemies[1])[1]]

    move = best_move(board, workers, enemy_reaches)

    if not move:  # Algorithm could not find a good enough move
        return False, best_build(board, workers, worker_reaches, enemy_reaches)
    # Pick better move, the one leading to a higher worker
    elif workers[0].height > workers[1].height:
        board.move(workers[1], move[0], move[1])
    else:
        board.move(workers[0], move[0], move[1])
    # Detect win
    if 3 in [workers[0].height, workers[1].height]:
        game.is_over = True

    return False, board


def best_move(board, workers, enemy_reaches):
    """
    Attempt to find the best move using a greedy approach
    :param board: current state of the board
    :param workers: relevant workers
    :param enemy_reaches: reaches of enemy workers
    :return: the best move found
    """
    one_reach, two_reach = board.valid_moves(workers[0])[0], board.valid_moves(workers[1])[0]
    worker_one_level, worker_one_highest = highest_buildings(board, one_reach)
    worker_two_level, worker_two_highest = highest_buildings(board, two_reach)

    max_level = max(worker_one_level, worker_two_level)  # Get the highest current level of own workers
    highest = worker_one_highest, worker_two_highest

    intersection = set(highest[0]).intersection(*highest)  # Get common moves

    # Check a greedy move can be made
    if highest != ([], []):
        # Can't get any higher
        if max_level <= workers[0].height and max_level <= workers[1].height:
            return
        # Return move to the highest building
        elif highest[0] == highest[1]:
            return highest[0][0]
        elif len(intersection) > 0:
            potential_moves = []
            for move in intersection:
                if move not in enemy_reaches:  # Optimal move
                    return move
                else:
                    potential_moves.append(move)  # Ideal if optimal not found
            # Optimal not found but ideal moves do exist
            if potential_moves:
                if len(potential_moves) > 1:  # Pick first move
                    return potential_moves[0]
                else:
                    return potential_moves


def best_build(board, workers, worker_reaches, enemy_reaches):
    """
    Attempt to find the best building possible for a given player
    :param board: current state of the board
    :param workers: desired workers
    :param worker_reaches: all possible build locations for the workers
    :param enemy_reaches: all possible move locations for the enemy workers
    :return: the updated board with the best found building
    """
    worker_heights = (workers[0].height, workers[1].height)

    # If worker can build higher than current level by one then do it
    for reach in worker_reaches:
        for move in reach:
            if move in board.buildings and board.board[move[0]][move[1]].height + 1 in worker_heights:
                board.build(move[0], move[1])
                return board

    intersection = set(worker_reaches[0]).intersection(*worker_reaches)
    # Build in reach of player
    if len(intersection) > 0:
        valid_moves = []
        for move in intersection:
            # Optimal building not accessible by enemy
            if move not in enemy_reaches:
                board.build(move[0], move[1])
                return board
            else:
                valid_moves.append(move)
        if valid_moves:
            if len(valid_moves) > 1:
                board.build(valid_moves[0], valid_moves[1])
                return board
            else:
                board.build(valid_moves[0], valid_moves[1])
                return board

    board.build(worker_reaches[0][0][0], worker_reaches[0][0][1])
    return board


def highest_buildings(board, reach):
    """
    Given the current state of the board and the desired reach return the reachable highest positions
    :param board: current state of the board
    :param reach: desired reach
    :return: the highest level and a list of the highest buildings on the board
    """
    highest = []
    level = 0

    for location in reach:
        if location in board.buildings:
            height = board.board[location[0]][location[1]].height
            if height < 4:
                if not highest:
                    highest, level = [location], height
                else:
                    for i in range(len(board.buildings) - 1):  # Already checked first building
                        if level < height:  # New building higher level so replace
                            highest, level = [location], height

                        elif level == height:  # New building same level so append
                            highest.append(location)

    return level, highest
