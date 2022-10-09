"""
This file is used to run the bots and decide the best moves based on the evaluations
"""
from AI.greedy import evaluateOptions, getHighest
from AI.minimax import minimax, decideWorker
from Game.actions import workerMove, workerBuild
from Game.ui import displayBoard


def mediumAI(startPos, player):
    """
    Uses the minimax algorithm to perform the best move for the given player and their current position

    :param startPos: A list containing the starting positions of players workers in format of [[0, 0], [1, 1]]
    :param player: The player to perform the action for
    :return: A list containing the new current positions
    """
    # A/C Evaluations
    xMoveEval = minimax(startPos[0], 3, -1000, 1000, 0, True, True, player)
    xBuildEval = minimax(startPos[0], 3, -1000, 1000, 0, False, True, player)

    # B/D Evaluations
    yMoveEval = minimax(startPos[1], 3, -1000, 1000, 1, True, True, player)
    yBuildEval = minimax(startPos[1], 3, -1000, 1000, 1, False, True, player)

    # See breakdowns of evaluations
    # print("Worker {}, Move Score: {}".format(player[0], xMoveEval))
    # print("Worker {}, Build Score: {}".format(player[0], xBuildEval))
    # print("Worker {}, Move Score: {}".format(player[1], yMoveEval))
    # print("Worker {}, Build Score: {}".format(player[1], yBuildEval))

    # Decide best evaluation
    bestMoveEval = decideWorker(yMoveEval, xMoveEval)
    bestBuildEval = decideWorker(yBuildEval, xBuildEval)

    if bestMoveEval[0][1] == [] and bestBuildEval[0][1] == []:  # Player has no options
        print("\nPlayer {}, has lost!".format(player[2]))
        exit()
    elif bestMoveEval[0][0] > bestBuildEval[0][0]:
        worker = bestMoveEval[1]
        print("{} moving to {}".format(player[worker], bestMoveEval[0][1]))
        startPos[worker] = workerMove(player, startPos[worker], worker, bestMoveEval[0][1])
    else:
        print("{} building at {}".format(player[bestBuildEval[1]], bestBuildEval[0][1]))
        workerBuild(bestBuildEval[0][1])

    displayBoard()
    return startPos


def easyAI(startPos, player):
    """
    Use factors of the current positions surroundings to decide the next best move, uses a greedy approach

    :param startPos: The initial positions of both workers
    :param player: The players whose move it is
    :return: The updated starting positions
    """
    highest = getHighest()

    xLevel, yLevel = int(player[0][3]), int(player[1][3])
    xEvaluation = evaluateOptions(highest, startPos[0], xLevel, 1)
    yEvaluation = evaluateOptions(highest, startPos[1], yLevel, 0)

    if xEvaluation[1] == 0 and yEvaluation[1] == 0:
        print("\nPlayer {}, has lost!!".format(player[2]))
        exit()
    elif xEvaluation[1] > yEvaluation[1]:
        if xEvaluation[0]:
            print("{} moving to {}".format(player[0], xEvaluation[2]))
            startPos[0] = workerMove(player, startPos[0], 0, xEvaluation[2])
        else:
            print("{} building on {}".format(player[0], xEvaluation[2]))
            workerBuild(xEvaluation[2])
    else:
        if yEvaluation[0]:
            print("{} moving to {}".format(player[1], yEvaluation[2]))
            startPos[1] = workerMove(player, startPos[1], 1, yEvaluation[2])
        else:
            print("{} building on {}".format(player[1], yEvaluation[2]))
            workerBuild(yEvaluation[2])

    displayBoard()
    return startPos
