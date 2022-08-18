from game import workerLoc, board, workerBuild, workerMove, newPosition
from exceptions import SelectionError, BoundsError, SpaceTakenError
from ui import getStartPos, displayBoard


def prepPlayer(player):
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
            displayBoard(board)

            worker = input("Select worker, {} or {} ? ".format(player[0], player[1]))

            # Player selected invalid character
            if worker not in ["A", "B", "C", "D"]:
                print("Fault 1")
                raise SelectionError

            active = findWorkerIndex(worker)[0]
            decision = input("Move or Build? ")

            activeStartPos = startPos[active]  # Start position of selected worker

            if decision == "Move":
                newPos = newPosition(input("Direction? "), activeStartPos)
                startPos[active] = workerMove(player, activeStartPos, active, newPos)

            elif decision == "Build":
                newPos = newPosition(input("Direction? "), activeStartPos)
                workerBuild(newPos)

            else:
                print("Fault 2")
                raise SelectionError

            displayBoard(board)

            return startPos

        except BoundsError:
            print("Out of bounds, please try again")
        except SpaceTakenError:
            print("Space taken, please try again")
        except SelectionError:
            print("Invalid selection, please try again.")


def findWorkerIndex(worker):
    """Find the index of the specified workers"""
    if worker == "A" or worker == "C":
        active, static = 0, 1
    elif worker == "B" or worker == "D":
        active, static = 1, 0
    else:
        raise SelectionError

    return active, static
