from game import newPosition, findBuildLevel, findLevelIndex, getWorkerLoc, getBuildLoc, getMoves, workerMove, \
    workerBuild

posInf = 2000
negInf = -2000


def possiblePositions(startPos, player):
    """Find all potential moves for a specified worker"""
    move, build = [], []

    for op in getMoves():
        pos = newPosition(op, startPos)

        if pos not in getWorkerLoc() and not any(0 > val for val in pos) and not any(
                val > 4 for val in pos):  # Looking for valid spaces
            build.append(pos)  # Can build anywhere in bounds and without a worker
            levelIndex = findLevelIndex(player[0])[2]

            if pos not in getBuildLoc() or findBuildLevel(pos) > player[levelIndex]:  # Can move/climb

                move.append(pos)

    return move, build


def runMiniMax(currentPos, player):
    moveEval = minimax(currentPos, 2, negInf, posInf, player, True, True)
    print("Best movement Pos: {}".format(moveEval[1]))
    print("Movement score: {}".format(moveEval[0]))

    buildEval = minimax(currentPos, 2, negInf, posInf, player, False, True)
    print("Best building Pos: {}".format(buildEval[1]))
    print("building score: {}".format(buildEval[0]))

    if moveEval[0] > buildEval[0]:
        print("Moving: {}".format(moveEval[1]))
        workerMove(player, currentPos, 0, moveEval[1])
    else:
        print("Building: {}".format(buildEval[1]))
        workerBuild(buildEval[1])

    return currentPos


def minimax(pos, depth, alpha, beta, currentPlayer, movement, maxPlayer):
    """Pos is the position to be evaluated, depth is the number of nodes to test, alpha and beta are to track for
    pruning, activePlayer is the player reference and maxPlayer represents whether aiming to maximise or minimise.

    Movement represents working/climbing (0) or building (1)"""
    if depth == 0:  # Reached end of search
        levelIndex = findLevelIndex(currentPlayer[0])[2]
        if movement:
            return [movementEvaluation(pos, currentPlayer[levelIndex]), pos]
        else:
            return [buildEvaluation(pos, currentPlayer[levelIndex]), pos]

    children = possiblePositions(pos, currentPlayer)[movement]
    bestPos = []

    # Need to maximise
    if maxPlayer:
        maxEval = negInf
        for child in children:
            # Recursive call for min search
            currentEval = minimax(child, depth - 1, alpha, beta, currentPlayer, movement, False)[0]
            if child in getBuildLoc():
                currentEval += 50

            maxEval = max(maxEval, currentEval)
            alpha = max(alpha, currentEval)

            if maxEval == currentEval:
                bestPos = child
            if beta <= alpha:
                break  # Prune remaining children
        return [maxEval, bestPos]

    else:  # Minimising
        minEval = posInf
        for child in children:
            # Recursive call for max search
            currentEval = minimax(child, depth - 1, alpha, beta, currentPlayer, movement, True)[0]
            if child in getBuildLoc():
                currentEval += 50

            minEval = min(minEval, currentEval)
            beta = min(beta, minEval)

            if minEval == currentEval:
                bestPos = child
            if beta <= alpha:
                break
        return [minEval, bestPos]


def movementEvaluation(position, workerLevel):
    levelScore = 0
    buildingScore = 0
    threatScore = 0

    # Add points depending upon workers current level
    match workerLevel:
        case 1:
            levelScore += 50
        case 2:
            levelScore += 80
        case 3:
            levelScore += 1000

    # Points for surrounding buildings
    for op in getMoves():
        pos = newPosition(op, position)

        if pos in getBuildLoc():
            buildLevel = findBuildLevel(pos)

            if workerLevel == buildLevel:
                buildingScore += 5
            else:
                threatScore += 1
                if workerLevel + 1 == buildLevel:
                    buildingScore += 15
                elif workerLevel + 2 == buildLevel:
                    buildingScore -= 15
                elif workerLevel + 3 == buildLevel:
                    buildingScore -= 20

    # Raise awareness of near win
    if workerLevel == 2 and threatScore >= 2:
        threatScore = 500

    return levelScore + buildingScore + threatScore


def buildEvaluation(position, workerLevel):
    enemyPos = getWorkerLoc()[:2]
    accessScore = 0
    enemyScore = 0
    friendScore = 0

    # Evaluate closeness to friend -> If friend can interact with space -> else direction of friend

    for op in getMoves():
        pos = newPosition(op, position)
        
        if pos in enemyPos:
            enemyScore -= 5

        elif pos in getBuildLoc():
            buildLevel = findBuildLevel(pos)
            if buildLevel == workerLevel:
                accessScore += 3
            elif buildLevel + 1 == workerLevel:
                accessScore += 2
            elif buildLevel + 2 == workerLevel:
                accessScore += 1

    return accessScore + enemyScore + friendScore


def beam():
    return


def monte():
    return
