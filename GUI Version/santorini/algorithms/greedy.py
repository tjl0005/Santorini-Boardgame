from ..constants import player_one, player_two


# Need to optimise
def greedy(board, player):
    if player == player_two:
        enemy = player_one
    else:
        enemy = player_two

    workers = board.get_player_workers(player_two)
    worker_reaches = [board.get_valid_moves(workers[0])[1], board.get_valid_moves(workers[1])[1]]
    enemies = board.get_player_workers(enemy)
    enemy_reaches = [board.get_valid_moves(enemies[0])[1] + board.get_valid_moves(enemies[1])[1]]

    move = best_move(board, workers, enemy_reaches)

    if not move:
        return best_build(board, workers, worker_reaches, enemy_reaches)

    if workers[0].height > workers[1].height:
        board.move(workers[1], move[0], move[1])
    else:
        board.move(workers[0], move[0], move[1])

    return board


def best_move(board, workers, enemy_reaches):
    one_reach, two_reach = board.get_valid_moves(workers[0])[0], board.get_valid_moves(workers[1])[0]
    worker_one_level, worker_one_highest = highest_buildings(board, one_reach)
    worker_two_level, worker_two_highest = highest_buildings(board, two_reach)

    max_level = max(worker_one_level, worker_two_level)
    highest = worker_one_highest, worker_two_highest

    intersection = set(highest[0]).intersection(*highest)

    if highest != ([], []):
        print("Max Level: {}".format(max_level))
        print("Current Levels: {}, {}".format(workers[0].height, workers[1].height))
        if max_level <= workers[0].height and max_level <= workers[1].height:
            print("Levels worse")
            return
        elif highest[0] == highest[1]:
            print("4")
            return highest[0][0]
        elif len(intersection) > 0:
            potential_moves = []
            for move in intersection:
                if move not in enemy_reaches:
                    return move
                else:
                    potential_moves.append(move)
            if potential_moves:
                if len(potential_moves) > 1:
                    return potential_moves[0]
                else:
                    return potential_moves


def best_build(board, workers, worker_reaches, enemy_reaches):
    worker_heights = (workers[0].height, workers[1].height)

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
    highest = []
    level = 0

    for location in reach:
        # print("Testing location: {}".format(location))
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
