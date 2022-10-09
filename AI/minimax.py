"""
This file contains the code to perform the minimax algorithm to evaluate all the potential moves of the workers
of the selected player
"""
from Game.player import getPlayerOne, getPlayerTwo
from Game.actions import newPosition, workerLoc, outBounds, maxHeight, getLevelFromBoard

moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]
playerOne, playerTwo = getPlayerOne(), getPlayerTwo()


def decideWorker(xEval, yEval):
    """
    Given two minimax evaluations return the higher scoring one and the relevant worker

    :param xEval: Either worker A or C's minimax evaluation
    :param yEval: Either worker B or D's minimax evaluation
    :return: A list containing the best static evaluation of those given and an integer representing the relevant worker
    """
    if xEval[0] > yEval[0]:
        return xEval, 1
    else:
        return yEval, 0


def reach(startPos, workerLevel):
    """
    Return the move and build reach of a worker given the workers current position and their level

    :param startPos: The initial coordinates of the worker
    :param workerLevel: The current level of the worker
    :return: Two lists containing the build and move reach
    """
    moveReach, buildReach = [], []
    for op in moves:
        pos = newPosition(op, startPos)
        # Position in bounds, not occupied by worker and not already realised
        if posValid(pos):
            buildReach.append(pos)
            posLevel = getLevelFromBoard(pos)
            if posLevel > 0:
                # Can climb or descend
                if workerLevel > posLevel < workerLevel or posLevel in [workerLevel, workerLevel + 1]:
                    moveReach.append(pos)
            else:  # Can move or move
                moveReach.append(pos)

    return buildReach, moveReach


def minimax(pos, depth, alpha, beta, refIndex, movement, maximising, player):
    """
    An implementation of the MiniMax algorithm to evaluate potential positions of a worker

    :param pos: The position to evaluate
    :param depth: Depth of the tree (Usually 3)
    :param alpha: negInf, used for alpha-beta pruning
    :param beta: maxInf, used for alpha-beta pruning
    :param refIndex: The relevant workers index within the player variable
    :param movement: Either evaluating board traversal (True) or building (False)
    :param maximising: True
    :param player: Relevant player variable
    :return: A list containing the static evaluation of the best position and the best found position
    """
    newLevel = getLevelFromBoard(pos)

    children = reach(pos, int(player[refIndex][3]))[movement]
    bestMove = []

    if depth == 0:  # Reached end of search
        if movement:
            # print("Pos: {} at level: {}".format(pos, newLevel))
            return movementEvaluation(children, int(player[refIndex][3]), newLevel), pos
        else:
            if player == playerTwo:
                opponent = playerOne
            else:
                opponent = playerTwo
            return buildEvaluation(pos, newLevel, opponent), pos

    elif maximising:
        maxEval = -1000
        for child in children:
            # Recursive call for min search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, False, player)[0]
            if currentEval > maxEval:
                maxEval = currentEval
                bestMove = child
            alpha = max(alpha, currentEval)

            if beta <= alpha:
                break  # Prune remaining children

        return maxEval, bestMove

    else:  # Minimising
        minEval = 1000
        for child in children:
            # Recursive call for max search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, True, player)[0]
            if currentEval < minEval:
                minEval = currentEval
                bestMove = child
            beta = min(beta, currentEval)

            if beta <= alpha:
                break

        return minEval, bestMove


def movementEvaluation(workerReach, oldLevel, newLevel):
    """
    Generate a score using the reach of a given position to see the "goodness" of the position overall

    :param workerReach: The reach of the selected position
    :param oldLevel: The current workers level
    :param newLevel: The current workers new level
    :return: An integer representing the score based on the reach and current positions height
    """
    buildingScore = 0
    levelScore = matchLevel(newLevel) - matchLevel(oldLevel)

    for pos in workerReach:
        posLevel = getLevelFromBoard(pos)
        if posLevel > 0:
            if newLevel + 1 == posLevel:
                buildingScore += 5
            elif newLevel + 2 == posLevel:
                buildingScore -= 5
            elif newLevel + 3 == posLevel:
                buildingScore -= 10

    # Final build and level scores
    return buildingScore + levelScore


def matchLevel(level):
    """
    Return a score based on a workers current level. A list of levels for a players workers must be given.

    :return: An integer representing the score
    """
    match level:
        case 1:
            return 30
        case 2:
            return 100
        case 3:
            return 1000
        case _:
            return 0


def buildEvaluation(buildPos, workerLevel, opponent):
    """
    Return a score based on a current positions surroundings for building

    :param buildPos: Position to be evaluated
    :param workerLevel: The current workers level
    :param opponent: The opponent of the current player
    :return: An integer representing the score based on the reach and current positions height
    """
    enemyLoc = getPlayerLoc(opponent)
    enemyHeight = [int(opponent[0][3]), int(opponent[1][3])]
    enemyReach = [reach(enemyLoc[0], enemyHeight[0])[0], reach(enemyLoc[0], enemyHeight[1])[0]]
    enemyScore, accessScore = 0, 0

    if buildPos in enemyReach[0] or buildPos in enemyReach[1]:  # Negate points if building in reach of enemy
        enemyScore += 5

    posLevel = getLevelFromBoard(buildPos)
    if posLevel != 0 and buildPos not in enemyLoc:  # Points if a building reachable
        if posLevel != 3:
            if posLevel == workerLevel:
                accessScore += 20
            elif posLevel - 1 == workerLevel:
                accessScore += 10

    if accessScore == 0:
        return 1
    return accessScore - enemyScore


def posValid(pos):
    """
    Check if a position is valid, meaning in bounds, not a dome and not occupied by a worker

    :return: True if the given position is valid, if not no return is given
    """
    if pos not in workerLoc and not outBounds(pos) and not maxHeight(pos):
        return True


def getPlayerLoc(player):
    """
    Given a player get the locations of their workers

    :return: A list containing the locations of the workers
    """
    playerLoc = [workerLoc[2], workerLoc[3]]

    if player == playerOne:
        playerLoc = [workerLoc[0], workerLoc[1]]

    return playerLoc
