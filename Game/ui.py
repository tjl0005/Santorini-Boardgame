"""
Used to output game messages such as the boards current state and use user inputs such as getting the start positions
of the players
"""
from Game.actions import outBounds, board
from Misc.exceptions import SpaceTakenError, SelectionError


def getStartPos(player, workerLoc):
    """
    Get the starting positions for a player from the user

    :param player: The player to get start positions for
    :param workerLoc: Record of workers locations
    :return: A list containing the formatted coordinates e.g. [[0,0], [1,1]]
    """
    while True:
        try:
            # PLayer selects their starting position, which is split
            posOne = input("Select starting position (e.g. 2,2) for {}: ".format(player[0])).split(",")
            posOne = [int(posOne[0]), int(posOne[1])]

            posTwo = input("Select starting position (e.g. 1,1) for {}: ".format(player[1])).split(",")
            posTwo = [int(posTwo[0]), int(posTwo[1])]

            check = checkStart(posOne, posTwo, workerLoc)

            return check

        except ValueError:
            print("One of more selections were invalid, please try again.".format(player))
        except IndexError:
            print("Please match requested format, please try again")
        except SpaceTakenError:
            print("A space you selected is taken, please try again")
        except SelectionError:
            print("Please enter a valid position")


def checkStart(posOne, posTwo, workerLoc):
    """
    Given two positions and the current worker locations (If any) ensure the positions are valid

    :param posOne: First workers position
    :param posTwo: Second workers position
    :param workerLoc: The current worker locations
    :return: The valid positions
    """
    if posOne == posTwo:  # Current player already taken the space
        raise SpaceTakenError
    elif posOne in workerLoc or posTwo in workerLoc:  # Other player taken the space
        raise SpaceTakenError
    elif outBounds(posOne) or outBounds(posTwo):  # Given positions out of bounds
        raise SelectionError
    else:  # Valid position given
        validPos = posOne, posTwo
        # Track all starting positions
        workerLoc.append(validPos[0])
        workerLoc.append(validPos[1])

        return validPos


def displayBoard():
    """
    Display the board properly in the console
    """
    for i in board:
        print("------ ------ ------ ------ ------")
        print(" ".join(i))

    print("------ ------ ------ ------ ------")


def moveCounter(count):
    """
    Increment the counter tracking the number of moves taken and print the new amount

    :param count: Number of moves taken
    :return: Updated count
    """
    count += 1
    print("Move Count: {}".format(count))
    return count


def selectWorker(player):
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


def selectAction():
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


def userDecideStartPos():
    """
    Ask user if they want to select the starting positions

    :return: True or False
    """
    if input("Select starting positions? (y/n) ") in ["y", "Y", "yes", "Yes"]:
        return True
    else:
        return False
