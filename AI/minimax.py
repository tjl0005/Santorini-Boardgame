"""
This file contains the code to perform the minimax algorithm to evaluate all the potential moves of the workers
of the selected player
"""
from Game.options import workerMove, newPosition, buildLoc, findBuildLevel, workerBuild, workerLoc, outBounds, maxHeight
from Game.player import getPlayerOne, getPlayerTwo
from Game.ui import displayBoard

posInf, negInf = 1000, -1000
moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]
playerOne, playerTwo = getPlayerOne(), getPlayerTwo()
# NOTE: Intending to test importance of central control
center = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]


def mediumAI(startPos, player):
    """
    Uses the minimax algorithm to perform the best move for the given player and their current position
    :param startPos: A list containing the starting positions of players workers in format of [[0, 0], [1, 1]]
    :param player: The player to perform the action for
    :return: A list containing the new current positions
    """
    # A/C Evaluations
    xMoveEval = minimax(startPos[0], 3, negInf, posInf, 0, True, True, player)
    xBuildEval = minimax(startPos[0], 3, negInf, posInf, 0, False, True, player)

    # B/D Evaluations
    yMoveEval = minimax(startPos[1], 3, negInf, posInf, 1, True, True, player)
    yBuildEval = minimax(startPos[1], 3, negInf, posInf, 1, False, True, player)

    print("Worker {}, Move Score: {}".format(player[0], xMoveEval))
    print("Worker {}, Build Score: {}".format(player[0], xBuildEval))
    print("Worker {}, Move Score: {}".format(player[1], yMoveEval))
    print("Worker {}, Build Score: {}".format(player[1], yBuildEval))

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


def reach(startPos, cLevel):
    """
    Return the move and build reach of a worker given the workers current position and their level
    :param startPos: The initial coordinates of the worker
    :param cLevel: The current level of the worker
    :return: Two lists containing the build and move reach
    """
    moveReach, buildReach = [], []
    for op in moves:
        pos = newPosition(op, startPos)
        # Position in bounds, not occupied by worker and not already realised
        if posValid(pos):
            buildReach.append(pos)
            if pos in buildLoc:
                bLevel = findBuildLevel(pos)
                if cLevel > bLevel < cLevel or bLevel in [cLevel, cLevel + 1]:  # Can climb/descend
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
    :param refIndex: The desired workers index within the player variable
    :param movement: Either board traversal (True) or building (False)
    :param maximising: True
    :param player: Relevant player variable
    :return: A list containing the static evaluation of the best position and the best found position
    """
    level = int(player[refIndex][3])
    opponent = playerTwo

    if player == playerTwo:
        opponent = playerOne
    if pos in buildLoc:
        level = findBuildLevel(pos)

    children = reach(pos, level)[movement]
    bestMove = []

    if depth == 0:  # Reached end of search
        if movement:
            return movementEvaluation(children, pos, level, refIndex, player, opponent)
        else:
            return buildEvaluation(children, pos, level, refIndex, player, opponent)

    if maximising:
        maxEval = negInf
        for child in children:
            # Recursive call for min search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, False, opponent)
            if currentEval > maxEval:
                maxEval = currentEval
                bestMove = child
                if maxEval > alpha:
                    alpha = maxEval

            if beta <= alpha:
                break  # Prune remaining children

        return [maxEval, bestMove]

    else:  # Minimising
        minEval = posInf
        for child in children:
            # Recursive call for max search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, True, opponent)[0]
            if currentEval < minEval:
                minEval = currentEval
                if minEval < beta:
                    beta = minEval

            if beta <= alpha:
                break

        return minEval


def movementEvaluation(currentReach, loc, workerLevel, refIndex, player, opponent):
    """
    Generate a score using the reach of a given position to see the "goodness" of the position overall
    :param currentReach: The reach of the selected position
    :param loc: The current position
    :param workerLevel: The current workers level
    :param refIndex: The workers index within the player variable
    :param player: The current player variable
    :param opponent: The opponents variable
    :return: An integer representing the score based on the reach and current positions height
    """
    playerLoc, playerHeight = getLocAndHeight(player, refIndex, workerLevel)
    playerReach = [reach(playerLoc[0], playerHeight[0])[1], reach(playerLoc[1], playerHeight[1])[1]]
    playerReach[refIndex], playerLoc[refIndex] = currentReach, loc

    enemyLoc, enemyHeight = getLocAndHeight(opponent, refIndex, -1)
    enemyReach = [reach(enemyLoc[0], enemyHeight[0])[1], reach(enemyLoc[1], enemyHeight[1])[1]]

    # TODO: Not using level of the tested position
    playerBuildScore, enemyBuildScore = moveScore(playerReach, playerHeight), moveScore(enemyReach, enemyHeight)
    playerHeightScore, enemyHeightScore = matchLevel(playerHeight), matchLevel(enemyHeight)

    playerScore = (playerBuildScore + playerHeightScore) - enemyHeightScore
    enemyScore = enemyBuildScore + enemyHeightScore

    playerScore = applyMultiplier(playerScore, 1.5)

    finalScore = calcFinalScore(playerScore, enemyScore)

    # Final build and level scores
    return finalScore


def moveScore(playerReach, workerLevel):
    """
    Assess the "goodness" of a positions surroundings
    :return: An integer representing the score based on the surrounding buildings of a worker
    """
    buildingScore, i = 0, 0
    for workerReach in playerReach:
        level = workerLevel[i]
        i += 1
        for pos in workerReach:
            if pos in buildLoc:
                buildLevel = findBuildLevel(pos)

                if buildLevel == 3 and level == 2:
                    buildingScore += 1000
                if level + 1 == buildLevel:
                    buildingScore += 20
                elif level + 2 == buildLevel:
                    buildingScore -= 10
                elif level + 3 == buildLevel:
                    buildingScore -= 15
                else:
                    buildingScore -= 20

    return buildingScore


def matchLevel(levels):
    """
    Return a score based on a workers current level. A list of levels for a players workers must be given.
    :return: An integer representing the score
    """
    score = 0
    for level in levels:
        match level:
            case 1:
                score += 100
            case 2:
                score += 200
            case 3:
                score += 1000
            case _:
                score += 0
    return score


def buildEvaluation(currentReach, loc, workerLevel, refIndex, player, opponent):
    """
    Return a score based on a current positions surroundings for building
    :param currentReach: The reach of the selected position
    :param loc: The current position
    :param workerLevel: The current workers level
    :param refIndex: The workers index within the player variable
    :param player: The current player
    :param opponent: The opponent of the current player
    :return: An integer representing the score based on the reach and current positions height
    """
    playerLoc, playerHeight = getLocAndHeight(player, refIndex, workerLevel)
    playerReach = [reach(playerLoc[0], playerHeight[0])[0], reach(playerLoc[0], playerHeight[1])[0]]
    playerReach[refIndex], playerLoc[refIndex] = currentReach, loc

    enemyLoc, enemyHeight = getLocAndHeight(opponent, refIndex, -1)
    enemyReach = [reach(enemyLoc[0], enemyHeight[0])[0], reach(enemyLoc[0], enemyHeight[1])[0]]

    playerEval = buildScore(playerReach, playerHeight, enemyReach, enemyLoc)
    enemyEval = buildScore(enemyReach, enemyHeight, playerReach, playerLoc)

    playerEval = applyMultiplier(playerEval, 1.5)

    finalScore = calcFinalScore(playerEval, enemyEval)

    # If there is no buildings and move evaluation low ensure a building will be constructed
    if playerEval <= 0:
        return 50

    return finalScore


def buildScore(playerReach, workerLevel, enemyReach, enemyLoc):
    """
    Assess the workers current surroundings with the goal of building
    :param playerReach: The selected players reach
    :param workerLevel: The current workers level
    :param enemyReach: Reach of the current players opponent
    :param enemyLoc: The locations of the current players opponent
    :return: An integer representing the score of the current player
    """
    enemyScore, accessScore, i, j = 0, 0, 0, 1
    for workerReach in playerReach:
        level = workerLevel[i]
        friendReach = playerReach[j]
        i += 1
        j -= 1
        for loc in workerReach:
            if loc in enemyReach[0] or loc in enemyReach[1]:  # Negate points if building in reach of enemy
                enemyScore -= 10
            elif loc in friendReach:
                enemyScore += 20

            if loc in buildLoc and loc not in enemyLoc:  # Points if a building reachable
                buildLevel = findBuildLevel(loc)
                if buildLevel != 3 and level != 0:
                    if buildLevel == 2 and level == 2:
                        accessScore += 200
                    if buildLevel == level:
                        accessScore += 20
                    elif buildLevel + 1 == level:
                        accessScore += 40
                    else:
                        accessScore -= 5

    return enemyScore + accessScore


def getLocAndHeight(player, i, update):
    """
    Given a player return the locations and heights of their workers
    :param player: The relevant player
    :param i: Flag if the height needs to be updated
    :param update: If the height needs to be updated, it will be updated to this
    :return: Tuple containing the locations and heights of the given player
    """
    loc = getPlayerLoc(player)
    height = [int(player[0][3]), int(player[1][3])]
    if update != -1:
        height[i] = update

    return loc, height


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


def calcFinalScore(playerScore, enemyScore):
    """
    Given the player and enemy score correctly combine them, for example avoiding a double negative
    :return: An integer representing the final score
    """
    if playerScore < 0 and enemyScore < 0 or playerScore > 0 > enemyScore:
        return playerScore + enemyScore
    else:
        return playerScore - enemyScore


def applyMultiplier(score, multiplier):
    """
    Given a score apply the given multiplier correctly, for example if a negative score the multiplier must be less than
    1
    :return: An integer representing the final score
    """
    if score < 0:
        return score * (multiplier - 1)
    else:
        return score * 1.5
