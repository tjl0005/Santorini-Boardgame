"""
This file contains the code to perform the minimax algorithm to evaluate all the potential moves of the workers
of the selected player
"""
from Game.player import get_player_one, get_player_two
from Game.actions import new_position, workerLoc, out_bounds, max_height, get_level_from_board

moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]
playerOne, playerTwo = get_player_one(), get_player_two()


def decide_worker(x_eval, y_eval):
    """
    Given two minimax evaluations return the higher scoring one and the relevant worker

    :param x_eval: Either worker A or C's minimax evaluation
    :param y_eval: Either worker B or D's minimax evaluation
    :return: A list containing the best static evaluation of those given and an integer representing the relevant worker
    """
    if x_eval[0] > y_eval[0]:
        return x_eval, 1
    else:
        return y_eval, 0


def reach(start_pos, worker_level):
    """
    Return the move and build reach of a worker given the workers current position and their level

    :param start_pos: The initial coordinates of the worker
    :param worker_level: The current level of the worker
    :return: Two lists containing the build and move reach
    """
    move_reach, build_reach = [], []
    for op in moves:
        pos = new_position(op, start_pos)
        # Position in bounds, not occupied by worker and not already realised
        if pos_valid(pos):
            build_reach.append(pos)
            pos_level = get_level_from_board(pos)
            if pos_level > 0:
                # Can climb or descend
                if worker_level > pos_level < worker_level or pos_level in [worker_level, worker_level + 1]:
                    move_reach.append(pos)
            else:  # Can move or move
                move_reach.append(pos)

    return build_reach, move_reach


def minimax(pos, depth, alpha, beta, ref_index, movement, maximising, player):
    """
    An implementation of the MiniMax algorithm to evaluate potential positions of a worker

    :param pos: The position to evaluate
    :param depth: Depth of the tree (Usually 3)
    :param alpha: negInf, used for alpha-beta pruning
    :param beta: maxInf, used for alpha-beta pruning
    :param ref_index: The relevant workers index within the player variable
    :param movement: Either evaluating board traversal (True) or building (False)
    :param maximising: True
    :param player: Relevant player variable
    :return: A list containing the static evaluation of the best position and the best found position
    """
    new_level = get_level_from_board(pos)

    children = reach(pos, int(player[ref_index][3]))[movement]
    best_move = []

    if depth == 0:  # Reached end of search
        if movement:
            # print("Pos: {} at level: {}".format(pos, new_level))
            return movement_evaluation(children, int(player[ref_index][3]), new_level), pos
        else:
            if player == playerTwo:
                opponent = playerOne
            else:
                opponent = playerTwo
            return build_evaluation(pos, new_level, opponent), pos

    elif maximising:
        max_eval = -1000
        for child in children:
            # Recursive call for min search
            current_eval = minimax(child, depth - 1, alpha, beta, ref_index, movement, False, player)[0]
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = child
            alpha = max(alpha, current_eval)

            if beta <= alpha:
                break  # Prune remaining children

        return max_eval, best_move

    else:  # Minimising
        min_eval = 1000
        for child in children:
            # Recursive call for max search
            current_eval = minimax(child, depth - 1, alpha, beta, ref_index, movement, True, player)[0]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = child
            beta = min(beta, current_eval)

            if beta <= alpha:
                break

        return min_eval, best_move


def movement_evaluation(worker_reach, old_level, new_level):
    """
    Generate a score using the reach of a given position to see the "goodness" of the position overall

    :param worker_reach: The reach of the selected position
    :param old_level: The current workers level
    :param new_level: The current workers new level
    :return: An integer representing the score based on the reach and current positions height
    """
    build_score = 0
    level_score = match_level(new_level) - match_level(old_level)

    for pos in worker_reach:
        pos_level = get_level_from_board(pos)
        if pos_level > 0:
            if new_level + 1 == pos_level:
                build_score += 5
            elif new_level + 2 == pos_level:
                build_score -= 5
            elif new_level + 3 == pos_level:
                build_score -= 10

    # Final build and level scores
    return build_score + level_score


def match_level(level):
    """
    Return a score based on a workers current level. A list of levels for a players workers must be given.

    :return: An integer representing the score
    """
    match level:
        case 1:
            return 30
        case 2:
            return 100
        case 3:
            return 1000
        case _:
            return 0


def build_evaluation(build_pos, worker_level, opponent):
    """
    Return a score based on a current positions surroundings for building

    :param build_pos: Position to be evaluated
    :param worker_level: The current workers level
    :param opponent: The opponent of the current player
    :return: An integer representing the score based on the reach and current positions height
    """
    enemy_loc = get_player_loc(opponent)
    enemy_height = [int(opponent[0][3]), int(opponent[1][3])]
    enemy_reach = [reach(enemy_loc[0], enemy_height[0])[0], reach(enemy_loc[0], enemy_height[1])[0]]
    enemy_score, access_score = 0, 0

    if build_pos in enemy_reach[0] or build_pos in enemy_reach[1]:  # Negate points if building in reach of enemy
        enemy_score += 5

    pos_level = get_level_from_board(build_pos)
    if pos_level != 0 and build_pos not in enemy_loc:  # Points if a building reachable
        if pos_level != 3:
            if pos_level == worker_level:
                access_score += 20
            elif pos_level - 1 == worker_level:
                access_score += 10

    if access_score == 0:
        return 1
    return access_score - enemy_score


def pos_valid(pos):
    """
    Check if a position is valid, meaning in bounds, not a dome and not occupied by a worker

    :return: True if the given position is valid, if not no return is given
    """
    if pos not in workerLoc and not out_bounds(pos) and not max_height(pos):
        return True


def get_player_loc(player):
    """
    Given a player get the locations of their workers

    :return: A list containing the locations of the workers
    """
    player_loc = [workerLoc[2], workerLoc[3]]

    if player == playerOne:
        player_loc = [workerLoc[0], workerLoc[1]]

    return player_loc
