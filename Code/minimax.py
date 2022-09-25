from player import getPlayerOne, getPlayerTwo
from game import newPosition, workerMove, workerBuild, findBuildLevel, outBounds, workerLoc, buildLoc, maxHeight

posInf = 1000
negInf = -1000
moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]
playerOne, playerTwo = getPlayerOne(), getPlayerTwo()


def reach(startPos, cLevel):
    """Returns a list of all possible positions for a worker"""
    moveReach, buildReach = [], []
    # Going through all adjacent spaces
    for op in moves:
        pos = newPosition(op, startPos)

        # Position in bounds, not occupied by worker and not already realised
        if pos not in workerLoc and not outBounds(pos) and not maxHeight(pos):
            buildReach.append(pos)
            if pos in buildLoc:
                bLevel = findBuildLevel(pos)

                if bLevel - 1 == cLevel or bLevel == cLevel:  # Can climb
                    moveReach.append(pos)

            else:  # Can move
                moveReach.append(pos)

    return moveReach, buildReach


def playMiniMax(startPos, refPlayer):
    if refPlayer == "One":
        player = playerOne
    else:
        player = playerTwo

    # A/C Evaluations
    xMoveEval = minimax(startPos[0], 2, negInf, posInf, 0, True, True, player)
    xBuildEval = minimax(startPos[0], 2, negInf, posInf, 0, False, True, player)
    # B/D Evaluations
    yMoveEval = minimax(startPos[1], 2, negInf, posInf, 1, True, True, player)
    yBuildEval = minimax(startPos[1], 2, negInf, posInf, 1, False, True, player)

    bestMoveEval = yMoveEval[1], 1
    bestBuildEval = yBuildEval[1], 1

    if xMoveEval > yMoveEval:
        bestMoveEval = xMoveEval[1], 0
    if xBuildEval > yBuildEval:
        bestBuildEval = xBuildEval[1], 0

    if xMoveEval > yBuildEval:
        worker = bestMoveEval[1]
        print("{} Moving {}".format(player[worker], bestMoveEval[0]))
        startPos[worker] = workerMove(player, startPos[worker], worker, bestMoveEval[0])
    else:
        worker = bestBuildEval[1]
        print("{} Building {}".format(player[worker], bestBuildEval[0]))
        workerBuild(bestBuildEval[0])

    return startPos


def minimax(pos, depth, alpha, beta, refIndex, movement, maximising, player):
    """Pos is the position to be evaluated, depth is the number of nodes to test, alpha and beta are to track for
    pruning, activePlayer is the player reference and maxPlayer represents whether aiming to maximise or minimise.

    Movement represents working/climbing (0) or building (1)"""
    level = int(player[refIndex][3])
    children = reach(pos, level)[movement]
    bestMove = []
    opponent = decidePlayer(player)

    # if pos == [2, 2] and "B" in player[refIndex]:
    #     print(children)
    #     print(level)
    #     print(findBuildLevel(pos))

    if depth == 0:  # Reached end of search
        if movement:
            return movementEvaluation(children, refIndex, player)
        else:
            return buildEvaluation(children, level)

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

        return maxEval, bestMove

    else:  # Minimising
        minEval = posInf
        for child in children:
            # Recursive call for max search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, True, opponent)

            minEval = min(minEval, currentEval)
            beta = min(beta, minEval)

            if beta <= alpha:
                break

        return minEval


def matchLevel(level):
    match level:
        case 1:
            return 20
        case 2:
            return 40
        case 3:
            return 1000
        case _:
            return 0


def movementEvaluation(currentReach, refIndex, player):
    """For a given possible position evaluate its effectiveness for movement"""
    levelScore, buildingScore = 0, 0

    enemyPlayer = decidePlayer(player)
    current = [int(player[0][3]), int(player[1][3])]
    currentLevel = current[refIndex]
    enemy = [int(enemyPlayer[0][3]), int(enemyPlayer[1][3])]
    levelScore += (matchLevel(current[0]) + matchLevel(current[1])) - (matchLevel(enemy[0]) + matchLevel(enemy[1]))

    # Points for surrounding buildings
    for pos in currentReach:
        if pos in buildLoc:
            buildLevel = findBuildLevel(pos)

            if currentLevel + 1 == buildLevel:
                buildingScore += 500
            elif currentLevel + 2 == buildLevel:
                buildingScore -= 10
            elif currentLevel + 3 == buildLevel:
                buildingScore -= 20

    # Win imminent
    if currentLevel == 3:
        return 1000

    # Building score the has the highest weighting
    finalScore = levelScore + buildingScore
    return finalScore


def buildEvaluation(currentReach, workerLevel):
    """For a given possible position evaluate its effectiveness for building"""
    accessScore, enemyScore = 0, 0

    # Find the reachable positions of other workers on the board
    enemyAReach, enemyBReach = reach(workerLoc[0], playerOne[3])[1], reach(workerLoc[1], playerOne[4])[1]

    for pos in currentReach:
        if pos in enemyAReach or pos in enemyBReach:  # Negate points if building in reach of enemy
            enemyScore -= 5

        if pos in buildLoc:  # Points if a building reachable
            buildLevel = findBuildLevel(pos)

            if buildLevel == workerLevel:
                accessScore += 100
            elif buildLevel + 1 == workerLevel:
                accessScore += 20
            elif buildLevel + 2 == workerLevel:
                accessScore += 15

    # If there is no buildings and move evaluation low ensure a building will be constructed
    if accessScore + enemyScore <= 0:
        return 10

    # Access score has the highest weighting
    return accessScore + enemyScore


def decidePlayer(ref):
    if ref == "One" or ref == playerTwo:
        return playerOne
    else:
        return playerTwo
