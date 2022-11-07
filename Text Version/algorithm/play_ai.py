"""
This file is used to run the bots and decide the best moves based on the evaluations
"""
from ..algorithm.greedy import evaluate_options, get_highest
from ..algorithm.minimax import minimax, decide_worker
from ..game.actions import worker_move, worker_build
from ..game.ui import display_board


def medium_ai(start_pos, player):
    """
    Uses the minimax algorithm to perform the best move for the given player and their current position

    :param start_pos: A list containing the starting positions of players workers in format of [[0, 0], [1, 1]]
    :param player: The player to perform the action for
    :return: A list containing the new current positions
    """
    # A/C Evaluations
    x_move_eval = minimax(start_pos[0], 3, -1000, 1000, 0, True, True, player)
    x_build_eval = minimax(start_pos[0], 3, -1000, 1000, 0, False, True, player)

    # B/D Evaluations
    y_move_eval = minimax(start_pos[1], 3, -1000, 1000, 1, True, True, player)
    y_build_eval = minimax(start_pos[1], 3, -1000, 1000, 1, False, True, player)

    # See breakdowns of evaluations
    # print("Worker {}, Move Score: {}".format(player[0], x_move_eval))
    # print("Worker {}, Build Score: {}".format(player[0], x_build_eval))
    # print("Worker {}, Move Score: {}".format(player[1], y_move_eval))
    # print("Worker {}, Build Score: {}".format(player[1], y_build_eval))

    # Decide best evaluation
    best_move_eval = decide_worker(y_move_eval, x_move_eval)
    best_build_eval = decide_worker(y_build_eval, x_build_eval)

    if best_move_eval[0][1] == [] and best_build_eval[0][1] == []:  # Player has no options
        print("\nPlayer {}, has lost!".format(player[2]))
        exit()
    elif best_move_eval[0][0] > best_build_eval[0][0]:
        worker = best_move_eval[1]
        print("{} moving to {}".format(player[worker], best_move_eval[0][1]))
        start_pos[worker] = worker_move(player, start_pos[worker], worker, best_move_eval[0][1])
    else:
        print("{} building at {}".format(player[best_build_eval[1]], best_build_eval[0][1]))
        worker_build(best_build_eval[0][1])

    display_board()
    return start_pos


def easy_ai(start_pos, player):
    """
    Use factors of the current positions surroundings to decide the next best move, uses a greedy approach

    :param start_pos: The initial positions of both workers
    :param player: The players whose move it is
    :return: The updated starting positions
    """
    highest = get_highest()

    x_level, y_level = int(player[0][3]), int(player[1][3])
    x_evaluation = evaluate_options(highest, start_pos[0], x_level, 1)
    y_evaluation = evaluate_options(highest, start_pos[1], y_level, 0)

    if x_evaluation[1] == 0 and y_evaluation[1] == 0:
        print("\nPlayer {}, has lost!!".format(player[2]))
        exit()
    elif x_evaluation[1] > y_evaluation[1]:
        if x_evaluation[0]:
            print("{} moving to {}".format(player[0], x_evaluation[2]))
            start_pos[0] = worker_move(player, start_pos[0], 0, x_evaluation[2])
        else:
            print("{} building on {}".format(player[0], x_evaluation[2]))
            worker_build(x_evaluation[2])
    else:
        if y_evaluation[0]:
            print("{} moving to {}".format(player[1], y_evaluation[2]))
            start_pos[1] = worker_move(player, start_pos[1], 1, y_evaluation[2])
        else:
            print("{} building on {}".format(player[1], y_evaluation[2]))
            worker_build(y_evaluation[2])

    display_board()
    return start_pos
