"""
This file is mainly used to initialise the players and to get the action selections from the user(s), but also
contains some essential functions used to improve functionality and accessibility of the player variables
"""
from ..game.actions import workerLoc, board, worker_move, new_position, worker_build
from ..game.ui import get_start_pos, display_board, select_worker, select_action
from ..misc.exceptions import SelectionError, BoundsError, SpaceTakenError

playerOne, playerTwo = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]


def set_board(player, user_select):
    """
    Given a player get the starting position from the user and update the board to represent the workers

    :param user_select: True, if user selecting starting positions or False if using default start
    :param player: Player whose workers need to be initialized
    :return: The selected starting positions
    """
    if user_select:
        pos_one, pos_two = get_start_pos(player, workerLoc)

    else:
        if player == playerOne:
            pos_one, pos_two = [1, 2], [2, 1]
        else:
            pos_one, pos_two = [2, 3], [3, 2]

        # Add new positions to workerLoc
        workerLoc.append(pos_one)
        workerLoc.append(pos_two)
        # Place workers on board
        board[pos_one[0]][pos_one[1]] = player[0]
        board[pos_two[0]][pos_two[1]] = player[1]

    return pos_one, pos_two


def player_choice(pos, player):
    """
    Present the user with their possible options and use their input to call the relevant action functions

    :param pos: The starting positions of the selected players workers
    :param player: The players whose turn it is
    :return: The updated starting position
    """
    while True:
        try:
            display_board()
            worker = select_worker(player)
            moving, direction = select_action()

            worker_index = find_worker_index(worker)[0]  # Get index of the selected worker
            worker_pos = pos[worker_index]  # Start position of selected worker

            if moving:
                # Moving means worker position needs to be updated
                pos[worker_index] = worker_move(player, worker_pos, worker_index, new_position(direction, worker_pos))
            elif not moving:
                # Position does not change when building
                worker_build(new_position(direction, worker_pos))
            else:
                print("Fault 2")
                raise SelectionError

            return pos

        except BoundsError:
            print("Out of bounds, please try again")
        except SpaceTakenError:
            print("Space taken, please try again")
        except SelectionError:
            print("Invalid selection, please try again.")


def find_worker_index(worker):
    """
    :param worker: The worker whose reference is unknown

    :return: The reference index of a selected worker
    """
    if worker in ["A", "C"]:
        return 0, 1
    elif worker in ["B", "D"]:
        return 1, 0
    else:
        raise SelectionError


def get_player_one():
    """
    :return: The current state of playerOne
    """
    return playerOne


def get_player_two():
    """
    :return: The current state of playerTwo
    """
    return playerTwo
