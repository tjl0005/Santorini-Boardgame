"""
Contains an implementation of minimax and the functions to properly evaluate any given state
"""
import copy

from ..utils.constants import PLAYER_TWO, PLAYER_ONE


def play(state, depth, alpha, beta, maximising, building, game):
    """
    Use the minimax algorithm with alpha-beta pruning
    :param state: current board state to evaluate
    :param depth: depth of the tree
    :param alpha: negInf, used for alpha-beta pruning
    :param beta: maxInf, used for alpha-beta pruning
    :param maximising: True, if evaluating AI player, false if evaluating an enemy player
    :param building: True, if evaluating building options, false if evaluating movement options
    :param game: The current game class
    :return: the evaluation (score) and the best state
    """
    best_state = None

    if depth == 0 or game.is_over:
        return evaluate(state), state

    # Maximising
    if maximising:
        max_eval = float('-inf')
        for state in get_states(state, PLAYER_TWO, building):
            new_eval = play(state, depth - 1, alpha, beta, False, building, game)[0]
            if new_eval > max_eval:
                max_eval = new_eval
                best_state = state
                print("New best move: {} {}".format(state.occupied, new_eval))
            elif max_eval > 1000:
                game.is_over = True
            alpha = max(alpha, new_eval)
            if beta <= alpha:
                break  # Prune remaining children

        return max_eval, best_state
    # Minimising
    else:
        min_eval = float('inf')
        for state in get_states(state, PLAYER_ONE, building):
            new_eval = play(state, depth - 1, alpha, beta, True, building, game)[0]
            min_eval = min(min_eval, new_eval)
            if new_eval < min_eval:
                min_eval = new_eval
                best_state = state
                print("New best move: {} {}".format(state.occupied, new_eval))

            elif min_eval > 1000:
                game.is_over = True

            beta = min(beta, new_eval)
            if beta <= alpha:
                break

        return min_eval, best_state


def simulate_move(piece, move, board):
    """
    Given a piece and new location simulate moving the piece with a deep copied board
    :param piece: piece to move
    :param move: new location
    :param board: deep copied board
    :return: updated copy of the board
    """
    board.action(piece, move[0], move[1])

    return board


def simulate_build(move, board):
    """
    Given a piece and new location simulate building with a deep copied board
    :param move: new location
    :param board: deep copied board
    :return: updated copy of the board
    """
    board.build(move[0], move[1])

    return board


def get_states(board, player, building):
    """
    Given the current board and player simulate all possible movements for different copys of the board (states) for
    either building (True) or moving (False)
    :param board: the current state of the board
    :param player: the player currently being evaluated
    :param building: True if evaluating building, False if evaluating moving
    :return:
    """
    outcome = []
    for worker in board.get_player_workers(player):
        valid_moves = board.get_valid_moves(worker)[building]
        for move in valid_moves:
            # X and Y coordinate are not out of bounds (Less than zero or grater than 5)
            if move[0] < 5 > move[1] > 0 < move[0]:
                # Simulate the move without editing current board
                test_board = copy.deepcopy(board)
                if building:
                    outcome.append(simulate_build(move, test_board))
                else:
                    test_piece = test_board.get_worker(worker.row, worker.col)
                    outcome.append(simulate_move(test_piece, move, test_board))

    return outcome


def height_evaluation(level):
    """
    Given a worker level return a score
    :param level: worker level
    :return: height score for the given worker
    """
    match level:
        case 1:
            return 60
        case 2:
            return 100
        case 3:
            return 1000
        case _:
            return 0
    

def evaluate(board):
    """
    Given the current state of the board evaluate the current state
    :param board: current state
    :return: final score for the given state
    """
    # Need to implement a near win solution
    height_score, build_score, near_win = 0, 0, 0
    # Store worker heights
    heights = board.player_one_heights + board.player_two_heights

    # Using relevant worker heights
    height_score = (height_evaluation(board.player_two_heights[0])) + (height_evaluation(board.player_two_heights[1]))
    # Using enemy heights
    enemy_score = (height_evaluation(board.player_one_heights[0])) + (height_evaluation(board.player_one_heights[1]))

    workers = board.get_player_workers(PLAYER_ONE) + board.get_player_workers(PLAYER_TWO)

    # Evaluate all workers on the board
    for worker in workers:
        index = workers.index(worker)
        reach = board.get_valid_moves(worker)[0]
        if index in [0, 1]:
            player = PLAYER_ONE
        else:
            player = PLAYER_TWO

        for move in reach:
            if move in board.buildings and move not in board.occupied:
                building_height = board.board[move[0]][move[1]].height
                score = 0
                if building_height < 4:
                    if building_height == heights[index] + 1:
                        score = 10
                    elif building_height == heights[index] + 2:
                        score = -5
                    elif building_height == heights[index] + 3:
                        score = -15

                if player == PLAYER_ONE:
                    enemy_score += score
                else:
                    build_score += score

    player_score = height_score + build_score

    if enemy_score > 0:
        player_score -= enemy_score
    else:
        player_score += enemy_score

    print("Height Score: {} and Build Score: {}".format(height_score, build_score))
    return height_score + build_score
