import copy

from ..constants import player_two, player_one


def minimax(state, depth, alpha, beta, maximising, building, game):
    best_state = None

    if depth == 0 or game.is_over:
        return evaluate(state), state

    # Maximising
    if maximising:
        max_eval = float('-inf')
        for state in get_states(state, player_two, building):
            new_eval = minimax(state, depth - 1, alpha, beta, False, building, game)[0]
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
        for state in get_states(state, player_one, building):
            new_eval = minimax(state, depth - 1, alpha, beta, True, building, game)[0]
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
    board.move(piece, move[0], move[1])

    return board


def simulate_build(move, board):
    board.build(move[0], move[1])

    return board


def get_states(board, player, building):
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
    # Need to implement a near win solution
    height_score, build_score, near_win = 0, 0, 0
    # Store worker heights
    heights = board.player_one_heights + board.player_two_heights

    # Using relevant worker heights
    height_score = (height_evaluation(board.player_two_heights[0])) + (height_evaluation(board.player_two_heights[1]))
    # Using enemy heights
    enemy_score = (height_evaluation(board.player_one_heights[0])) + (height_evaluation(board.player_one_heights[1]))

    workers = board.get_player_workers(player_one) + board.get_player_workers(player_two)

    # Evaluate all workers on the board
    for worker in workers:
        index = workers.index(worker)
        reach = board.get_valid_moves(worker)[0]
        if index in [0, 1]:
            player = player_one
        else:
            player = player_two

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

                if player == player_one:
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
