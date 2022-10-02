"""
This file is mainly used to initialise the players and to get the action selections from the user(s), but also
contains some essential functions used to improve functionality and accessibility of the player variables
"""
from Game.options import workerLoc, board, workerMove, newPosition, workerBuild
from Game.ui import getStartPos, displayBoard
from Misc.exceptions import SelectionError, BoundsError, SpaceTakenError

playerOne, playerTwo = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]


def setBoard(player):
    """
    Given a player get the starting position from the user and update the board to represent the workers
    :param player: Player whose workers need to be placed
    :return: The selected starting positions
    """
    startPos1, startPos2 = getStartPos(player, workerLoc)

    board[startPos1[0]][startPos1[1]] = player[0]
    board[startPos2[0]][startPos2[1]] = player[1]

    return startPos1, startPos2


def playerChoice(startPos, player):
    """
    Present the user with their possible options and use their input to call the relevant action functions
    :param startPos: The starting positions of the selected players workers
    :param player: The players whose turn it is
    :return: The updated starting position
    """
    while True:
        try:
            displayBoard()
            worker = input("Select worker, {} or {} ? ".format(player[0], player[1]))

            # Player selected invalid character
            if worker not in ["A", "B", "C", "D"]:
                print("Fault 1")
                raise SelectionError

            selIndex = findWorkerIndex(worker)[0]  # Get index of the selected worker
            selPos = startPos[selIndex]  # Start position of selected worker

            decision = input("Move or Build? ")

            if decision in ["Move", "move"]:
                startPos[selIndex] = workerMove(player, selPos, selIndex, newPosition(input("Direction? "), selPos))
            elif decision in ["Build", "build"]:
                workerBuild(newPosition(input("Direction? "), selPos))
            else:
                print("Fault 2")
                raise SelectionError

            return startPos

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
