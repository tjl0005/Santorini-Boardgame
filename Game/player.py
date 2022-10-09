"""
This file is mainly used to initialise the players and to get the action selections from the user(s), but also
contains some essential functions used to improve functionality and accessibility of the player variables
"""
from Game.actions import workerLoc, board, workerMove, newPosition, workerBuild
from Game.ui import getStartPos, displayBoard, selectWorker, selectAction
from Misc.exceptions import SelectionError, BoundsError, SpaceTakenError

playerOne, playerTwo = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]


def setBoard(player, userSelect):
    """
    Given a player get the starting position from the user and update the board to represent the workers

    :param userSelect: True, if user selecting starting positions or False if using default start
    :param player: Player whose workers need to be initialized
    :return: The selected starting positions
    """
    if userSelect:
        posOne, posTwo = getStartPos(player, workerLoc)

    else:
        if player == playerOne:
            posOne, posTwo = [1, 2], [2, 1]
        else:
            posOne, posTwo = [2, 3], [3, 2]

        # Add new positions to workerLoc
        workerLoc.append(posOne)
        workerLoc.append(posTwo)
        # Place workers on board
        board[posOne[0]][posOne[1]] = player[0]
        board[posTwo[0]][posTwo[1]] = player[1]

    return posOne, posTwo


def playerChoice(pos, player):
    """
    Present the user with their possible options and use their input to call the relevant action functions

    :param pos: The starting positions of the selected players workers
    :param player: The players whose turn it is
    :return: The updated starting position
    """
    while True:
        try:
            displayBoard()
            worker = selectWorker(player)
            moving, direction = selectAction()

            workerIndex = findWorkerIndex(worker)[0]  # Get index of the selected worker
            workerPos = pos[workerIndex]  # Start position of selected worker

            if moving:
                # Moving means worker position needs to be updated
                pos[workerIndex] = workerMove(player, workerPos, workerIndex, newPosition(direction, workerPos))
            elif not moving:
                # Position does not change when building
                workerBuild(newPosition(direction, workerPos))
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


def findWorkerIndex(worker):
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


def getPlayerOne():
    """
    :return: The current state of playerOne
    """
    return playerOne


def getPlayerTwo():
    """
    :return: The current state of playerTwo
    """
    return playerTwo
