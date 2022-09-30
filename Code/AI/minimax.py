from Code.Game.playOptions import workerMove, newPosition, buildLoc, findBuildLevel, workerBuild, workerLoc, outBounds, maxHeight
from Code.Game.player import getPlayerOne, getPlayerTwo
from Code.Game.ui import displayBoard

posInf, negInf = 1000, -1000
moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]
playerOne, playerTwo = getPlayerOne(), getPlayerTwo()
# NOTE: Intending to test importance of central control
center = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]


def mediumAI(startPos, player):
    """Operate the minimax function, find the best decision and act on it"""
    displayBoard()
    # A/C Evaluations
    xMoveEval = minimax(startPos[0], 3, negInf, posInf, 0, True, True, player)
    xBuildEval = minimax(startPos[0], 3, negInf, posInf, 0, False, True, player)

    # B/D Evaluations
    yMoveEval = minimax(startPos[1], 3, negInf, posInf, 1, True, True, player)
    yBuildEval = minimax(startPos[1], 3, negInf, posInf, 1, False, True, player)

    # print("Worker {}, Move Score: {}".format(player[0], xMoveEval))
    # print("Worker {}, Build Score: {}".format(player[0], xBuildEval))
    # print("Worker {}, Move Score: {}".format(player[1], yMoveEval))
    # print("Worker {}, Build Score: {}".format(player[1], yBuildEval))

    # Decide best evaluation
    bestMoveEval = decideWorker(yMoveEval, xMoveEval)
    bestBuildEval = decideWorker(yBuildEval, xBuildEval)

    if bestMoveEval[0][1] == [] and bestBuildEval[0][1] == []:  # Player has no options
        print("\nPlayer {}, has lost!!".format(player[2]))
        exit()
    elif bestMoveEval[0][0] > bestBuildEval[0][0]:
        worker = bestMoveEval[1]
        print("{} moving to {}".format(player[worker], bestMoveEval[0][1]))
        startPos[worker] = workerMove(player, startPos[worker], worker, bestMoveEval[0][1])
    else:
        print("{} building at {}".format(player[bestBuildEval[1]], bestBuildEval[0][1]))
        workerBuild(bestBuildEval[0][1])

    return startPos


def decideWorker(xEval, yEval):
    """Given the evaluations for both workers, return those that scored better"""
    if xEval[0] > yEval[0]:
        return xEval, 1
    else:
        return yEval, 0


def reach(startPos, cLevel):
    """Returns a list of all possible positions for a worker"""
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
    """Pos is the position to be evaluated, depth is the number of nodes to test, alpha and beta are to track for
    pruning, activePlayer is the player reference and maxPlayer represents whether aiming to maximise or minimise."""
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
            alpha = max(alpha, currentEval)

            if beta <= alpha:
                break  # Prune remaining children

        return [maxEval, bestMove]

    else:  # Minimising
        minEval = posInf
        for child in children:
            # Recursive call for max search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, True, opponent)[0]
            minEval = min(minEval, currentEval)
            beta = min(beta, minEval)

            if beta <= alpha:
                break

        return minEval


def movementEvaluation(currentReach, loc, workerLevel, refIndex, player, opponent):
    """For a given possible position evaluate its effectiveness for movement"""
    playerLoc, playerHeight = getLocAndHeight(player, refIndex, workerLevel)
    playerReach = [reach(playerLoc[0], playerHeight[0])[1], reach(playerLoc[1], playerHeight[1])[1]]
    playerReach[refIndex], playerLoc[refIndex] = currentReach, loc

    enemyLoc, enemyHeight = getLocAndHeight(opponent, refIndex, -1)
    enemyReach = [reach(enemyLoc[0], enemyHeight[0])[1], reach(enemyLoc[1], enemyHeight[1])[1]]

    playerBuildScore, enemyBuildScore = moveScore(playerReach, playerHeight), moveScore(enemyReach, enemyHeight)
    playerHeightScore, enemyHeightScore = matchLevel(playerHeight), matchLevel(enemyHeight)

    finalScore = (playerBuildScore - enemyBuildScore) + (playerHeightScore - enemyHeightScore)

    # Final build and level scores
    return finalScore


def moveScore(playerReach, workerLevel):
    """Return a score based on the buildings accessible within a workers current reach"""
    buildingScore, i = 0, 0
    for workerReach in playerReach:
        level = workerLevel[i]
        i += 1
        for pos in workerReach:
            if pos in buildLoc:
                buildLevel = findBuildLevel(pos)

                if level == 2 and buildLevel == 2:  # Near win
                    buildingScore += 500
                elif level + 1 == buildLevel:
                    buildingScore += 5
                elif level + 2 == buildLevel:
                    buildingScore -= 10
                elif level + 3 == buildLevel:
                    buildingScore -= 15
                else:
                    buildingScore -= 10
            if pos in center:
                buildingScore += 10

    return buildingScore


def matchLevel(levels):
    """Produce score depending upon building/worker level"""
    score = 0
    for level in levels:
        match level:
            case 1:
                score += 40
            case 2:
                score += 60
            case 3:
                score += 1000
            case _:
                score += 0
    return score


def buildEvaluation(currentReach, loc, workerLevel, refIndex, player, opponent):
    """For a given possible position evaluate its effectiveness for building"""
    playerLoc, playerHeight = getLocAndHeight(player, refIndex, workerLevel)
    playerReach = [reach(playerLoc[0], playerHeight[0])[0], reach(playerLoc[0], playerHeight[1])[0]]
    playerReach[refIndex], playerLoc[refIndex] = currentReach, loc

    enemyLoc, enemyHeight = getLocAndHeight(opponent, refIndex, -1)
    enemyReach = [reach(enemyLoc[0], enemyHeight[0])[0], reach(enemyLoc[0], enemyHeight[1])[0]]

    playerEval = buildScore(playerReach, playerHeight, enemyReach, enemyLoc)
    enemyEval = buildScore(enemyReach, enemyHeight, playerReach, playerLoc)

    finalScore = playerEval - enemyEval

    # If there is no buildings and move evaluation low ensure a building will be constructed
    if finalScore <= 0:
        return 10

    return finalScore


def buildScore(playerReach, workerLevel, enemyReach, enemyLoc):
    """Return a score based on the buildings accessible within a workers current reach"""
    enemyScore, accessScore, i = 0, 0, 0
    for workerReach in playerReach:
        level = workerLevel[i]
        i += 1
        for loc in workerReach:
            if loc in enemyReach[0] or loc in enemyReach[1]:  # Negate points if building in reach of enemy
                enemyScore -= 10

            if loc in buildLoc and loc not in enemyLoc:  # Points if a building reachable
                buildLevel = findBuildLevel(loc)
                if buildLevel != 3 and level != 0:
                    if buildLevel == level:
                        accessScore += 10
                    elif buildLevel + 1 == level:
                        accessScore += 5
                    else:
                        accessScore -= 5

    return enemyScore + accessScore


def getLocAndHeight(player, i, update):
    """Return the locations and heights of a selected player"""
    loc = getPlayerLoc(player)
    height = [int(player[0][3]), int(player[1][3])]
    if update != -1:
        height[i] = update

    return loc, height


def posValid(pos):
    """Check if a position is valid"""
    if pos not in workerLoc and not outBounds(pos) and not maxHeight(pos):
        return True


def getPlayerLoc(player):
    """For a given player return its workers locations"""
    playerLoc = [workerLoc[2], workerLoc[3]]

    if player == playerOne:
        playerLoc = [workerLoc[0], workerLoc[1]]

    return playerLoc
