"""
Used to output game messages such as the boards current state and use user inputs such as getting the start positions
of the players
"""
from Game.options import outBounds, board
from Misc.exceptions import SpaceTakenError, SelectionError


def getStartPos(player, workerPos):
    """
    Get the starting positions for a player from the user via inputs from the console
    :param player: The player to get the start positions for
    :param workerPos: The current locations of workers
    :return: A list containing the formatted coordinates e.g. [[0,0], [1,1]]
    """
    while True:
        try:
            # PLayer selects their starting position, which is split
            pos1 = input("Select starting position (e.g. 2,2) for {}: ".format(player[0])).split(",")
            pos1 = [int(pos1[0]), int(pos1[1])]

            pos2 = input("Select starting position (e.g. 1,1) for {}: ".format(player[1])).split(",")
            pos2 = [int(pos2[0]), int(pos2[1])]

            check = checkStart(pos1, pos2, workerPos)

            return check

        except ValueError:
            print("One of more selections were invalid, try again.".format(player))
        except IndexError:
            print("Please match requested format, try again")
        except SpaceTakenError:
            print("A space you selected is taken, please try again")
        except SelectionError:
            print("Please enter a valid position")


def checkStart(pos1, pos2, workerPos):
    """
    Given two positions and the current worker locations (If any) ensure the positions are valid
    :param pos1: First workers position
    :param pos2: Second workers position
    :param workerPos: The current worker locations
    :return: The valid positions
    """
    if pos1 == pos2:  # Current player already taken the space
        raise SpaceTakenError
    elif pos1 in workerPos or pos2 in workerPos:  # Other player taken the space
        raise SpaceTakenError
    elif outBounds(pos1) or outBounds(pos2):  # Given positions out of bounds
        raise SelectionError
    else:  # Valid position given
        validPos = pos1, pos2
        # Track all starting positions
        workerPos.append(validPos[0])
        workerPos.append(validPos[1])

        return validPos


def displayBoard():
    """
    Display the board properly in the console
    """
    for i in board:
        print("------ ------ ------ ------ ------")
        print(" ".join(i))

    print("------ ------ ------ ------ ------")
