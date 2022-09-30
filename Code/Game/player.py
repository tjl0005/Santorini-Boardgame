from Code.Game.playOptions import workerLoc, board, workerMove, newPosition, workerBuild
from Code.Game.ui import getStartPos, displayBoard
from Code.Misc.exceptions import SelectionError, BoundsError, SpaceTakenError

playerOne, playerTwo = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]


def setBoard(player):
    """Uses the setStart function twice to get the starting locations of each worker. The returned coordinates are then
    used to update the board with the locations of the workers and display them to the user."""
    startPos1, startPos2 = getStartPos(player, workerLoc)

    board[startPos1[0]][startPos1[1]] = player[0]
    board[startPos2[0]][startPos2[1]] = player[1]

    return startPos1, startPos2


def playerChoice(startPos, player):
    """Present player with possible options"""
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
    """Find the index of the specified workers"""
    if worker in ["A", "C"]:
        return 0, 1
    elif worker in ["B", "D"]:
        return 1, 0
    else:
        raise SelectionError


def getPlayerOne():
    return playerOne


def getPlayerTwo():
    return playerTwo
