from game import newPosition, findBuildLevel, findLevelIndex, getWorkerLoc, getBuildLoc, getMoves, workerMove, \
    workerBuild

posInf = 2000
negInf = -2000
moves = getMoves()


def possiblePositions(startPos, worker):
    """Find potential move and build options for a specified worker"""
    move, build = [], []
    workerLevel = int(worker[3])  # Always same index because the worker is specified

    for op in moves:
        pos = newPosition(op, startPos)

        # Looking for valid spaces
        if pos not in getWorkerLoc() and not any(0 > val for val in pos) and not any(val > 4 for val in pos):
            build.append(pos)  # Can build anywhere in bounds and without a worker

            if pos not in getBuildLoc() or findBuildLevel(pos) > workerLevel:  # Can move/climb
                move.append(pos)

    return move, build


def playAI(pos, selPlayer):
    """Currently set to run minimax"""
    # Get evaluations for both workers
    evaluations = [runMiniMax(pos[0], 0, selPlayer), runMiniMax(pos[1], 1, selPlayer)]
    worker = 1

    if evaluations[0][1][0] > evaluations[1][1][0]:  # Find if worker C or D has the better option and switch if nesc.
        worker = 0

    # Current worker position and the new position to either move to or build on
    workerPos = pos[worker]
    newPos = evaluations[worker][1][1]

    if evaluations[worker][0] == "move":
        pos[worker] = workerMove(selPlayer, workerPos, worker, newPos)
    else:
        workerBuild(newPos)

    return pos


def runMiniMax(currentPos, refIndex, selPlayer):
    """Calls the minimax algorithm to evaluate options for both workers and then makes the highest ranked move"""
    moveEval = minimax(currentPos, 2, negInf, posInf, refIndex, True, True, selPlayer)
    buildEval = minimax(currentPos, 2, negInf, posInf, refIndex, False, True, selPlayer)

    print("Worker: {}, move: {} and build: {}".format(selPlayer[refIndex], moveEval, buildEval))

    if moveEval[0] > buildEval[0]:
        return "move", moveEval
    else:
        return "build", buildEval


def minimax(pos, depth, alpha, beta, refIndex, movement, maxPlayer, player):
    """Pos is the position to be evaluated, depth is the number of nodes to test, alpha and beta are to track for
    pruning, activePlayer is the player reference and maxPlayer represents whether aiming to maximise or minimise.

    Movement represents working/climbing (0) or building (1)"""

    # If there are no buildings that can be reached need to build
    # o	Towards friend
    # o	Away from enemies
    # •	If next to same level building, build on it
    # o	If multiple pick one with most potential

    if depth == 0:  # Reached end of search
        levelIndex = findLevelIndex(player[refIndex])[2]
        if movement:
            return movementEvaluation(pos, player[levelIndex]), pos
        else:
            return buildEvaluation(pos, player[levelIndex]), pos

    children = possiblePositions(pos, player[refIndex])[movement]
    bestPos = []

    # Need to maximise
    if maxPlayer:
        maxEval = negInf
        for child in children:
            # Recursive call for min search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, False, player)[0]
            if child in getBuildLoc():
                currentEval += 50

            maxEval = max(maxEval, currentEval)
            alpha = max(alpha, currentEval)

            if maxEval == currentEval:
                bestPos = child
            if beta <= alpha:
                break  # Prune remaining children
        return maxEval, bestPos

    else:  # Minimising
        minEval = posInf
        for child in children:
            # Recursive call for max search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, True, player)[0]
            if child in getBuildLoc():
                currentEval += 50

            minEval = min(minEval, currentEval)
            beta = min(beta, minEval)

            if minEval == currentEval:
                bestPos = child
            if beta <= alpha:
                break
        return minEval, bestPos


def movementEvaluation(position, workerLevel):
    """For a given possible position evaluate its effectiveness for movement"""
    levelScore, buildingScore, threatScore = 0, 0, 0

    # Add points depending upon workers current level
    match workerLevel:
        case 1:
            levelScore += 30
        case 2:
            levelScore += 50
        case 3:
            levelScore += 1000

    # Points for surrounding buildings
    for op in moves:
        pos = newPosition(op, position)

        if pos in getBuildLoc():
            buildLevel = findBuildLevel(pos)

            if workerLevel == buildLevel:
                buildingScore += 5
            else:
                threatScore += 1
                if workerLevel + 1 == buildLevel:
                    buildingScore += 100
                elif workerLevel + 2 == buildLevel:
                    buildingScore -= 50
                elif workerLevel + 3 == buildLevel:
                    buildingScore -= 20

    # Raise awareness of near win
    if workerLevel == 2 and threatScore >= 2:
        threatScore = 500

    return levelScore + buildingScore + threatScore


def buildEvaluation(position, workerLevel):
    """For a given possible position evaluate its effectiveness for building"""
    enemyPos = getWorkerLoc()[:2]
    accessScore, enemyScore, friendScore = 0, 0, 0

    # Evaluate closeness to friend -> If friend can interact with space -> else direction of friend

    for op in moves:
        pos = newPosition(op, position)

        if pos in enemyPos:
            enemyScore -= 10

        elif pos in getBuildLoc():
            buildLevel = findBuildLevel(pos)
            if buildLevel == workerLevel:
                accessScore += 50
            elif buildLevel + 1 == workerLevel:
                accessScore += 30
            elif buildLevel + 2 == workerLevel:
                accessScore += 15

    return accessScore + enemyScore + friendScore


def beam():
    return


def monte():
    return
