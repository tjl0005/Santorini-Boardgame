"""
Used to output game messages such as the boards current state and use user inputs such as getting the start positions
of the players
"""
from ..game.actions import out_bounds, board
from ..misc.exceptions import SpaceTakenError, SelectionError


def get_start_pos(player, worker_loc):
    """
    Get the starting positions for a player from the user

    :param player: The player to get start positions for
    :param worker_loc: Record of workers locations
    :return: A list containing the formatted coordinates e.g. [[0,0], [1,1]]
    """
    while True:
        try:
            # PLayer selects their starting position, which is split
            pos_one = input("Select starting position (e.g. 2,2) for {}: ".format(player[0])).split(",")
            pos_one = [int(pos_one[0]), int(pos_one[1])]

            pos_two = input("Select starting position (e.g. 1,1) for {}: ".format(player[1])).split(",")
            pos_two = [int(pos_two[0]), int(pos_two[1])]

            check = check_start(pos_one, pos_two, worker_loc)

            return check

        except ValueError:
            print("One of more selections were invalid, please try again.".format(player))
        except IndexError:
            print("Please match requested format, please try again")
        except SpaceTakenError:
            print("A space you selected is taken, please try again")
        except SelectionError:
            print("Please enter a valid position")


def check_start(pos_one, pos_two, worker_loc):
    """
    Given two positions and the current worker locations (If any) ensure the positions are valid

    :param pos_one: First workers position
    :param pos_two: Second workers position
    :param worker_loc: The current worker locations
    :return: The valid positions
    """
    if pos_one == pos_two:  # Current player already taken the space
        raise SpaceTakenError
    elif pos_one in worker_loc or pos_two in worker_loc:  # Other player taken the space
        raise SpaceTakenError
    elif out_bounds(pos_one) or out_bounds(pos_two):  # Given positions out of bounds
        raise SelectionError
    else:  # Valid position given
        valid_pos = pos_one, pos_two
        # Track all starting positions
        worker_loc.append(valid_pos[0])
        worker_loc.append(valid_pos[1])

        return valid_pos


def display_board():
    """
    Display the board properly in the console
    """
    for i in board:
        print("------ ------ ------ ------ ------")
        print(" ".join(i))

    print("------ ------ ------ ------ ------")


def move_counter(count):
    """
    Increment the counter tracking the number of moves taken and print the new amount

    :param count: Number of moves taken
    :return: Updated count
    """
    count += 1
    print("Move Count: {}".format(count))
    return count


def select_worker(player):
    """
    Get user to select a worker

    :param player: The current player
    :return: The user selected worker
    """
    worker = input("Select worker, {} or {} ? ".format(player[0], player[1]))
    # Player selected invalid character
    if worker not in ["A", "B", "C", "D"]:
        print("Fault 1")
        raise SelectionError
    else:
        return worker


def select_action():
    """
    Get worker action from current user

    :return: True, to indicate movement or False, to indicate building
    """
    action = input("Move or Build? ")
    direction = input("Direction? ")

    if action in ["Move", "move"]:
        return True, direction
    elif action in ["Build", "build"]:
        return False, direction
    else:
        print("Fault 2")
        raise SelectionError


def user_decide_start_pos():
    """
    Ask user if they want to select the starting positions

    :return: True or False
    """
    if input("Select starting positions? (y/n) ") in ["y", "Y", "yes", "Yes"]:
        return True
    else:
        return False
