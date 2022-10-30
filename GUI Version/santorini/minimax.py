import copy

from .constants import player_two, player_one


def minimax(board, old_levels, worker_index, depth, alpha, beta, player, game):
    if depth == 0 or game.is_over:
        return board.movement_evaluation(worker_index, old_levels), board

    # Maximising
    if player:
        max_eval = float('-inf')
        best_state = None
        state_maps = get_states(board, player_two)
        for state in state_maps:
            worker_index = state_maps[state]
            new_eval = minimax(state, old_levels, worker_index, depth - 1, alpha, beta, False, game)[0]
            max_eval = max(max_eval, new_eval)
            if max_eval == new_eval:
                best_state = state

            alpha = max(alpha, new_eval)
            if beta <= alpha:
                break  # Prune remaining children

        return max_eval, best_state
    # Minimising
    else:
        min_eval = float('inf')
        best_state = None
        state_maps = get_states(board, player_one)
        for state in state_maps:
            worker_index = state_maps[state]
            new_eval = minimax(state, old_levels, worker_index, depth - 1, alpha, beta, True, game)[0]
            min_eval = min(min_eval, new_eval)
            if min_eval == new_eval:
                best_state = state

            beta = min(beta, new_eval)
            if beta <= alpha:
                break

        return min_eval, best_state


def simulate_move(piece, move, board):
    board.move(piece, move[0], move[1])

    return board


def get_states(board, player):
    state_map = {}

    for piece in board.get_player_workers(player):
        valid_moves = board.get_valid_moves(piece)[0]
        for move in valid_moves:
            # X and Y coordinate are not out of bounds (Less than zero or grater than 5)
            if move[0] < 5 > move[1] > 0 < move[0]:

                # Simulate the move without editing current board
                test_board = copy.deepcopy(board)
                test_piece = test_board.get_worker(piece.row, piece.col)
                outcome = simulate_move(test_piece, move, test_board)

                state_map[outcome] = test_piece.index

    return state_map
