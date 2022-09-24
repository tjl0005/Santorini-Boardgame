from player import getPlayerOne
from game import newPosition, workerMove, workerBuild, findBuildLevel, outBounds, workerLoc, buildLoc
from ui import displayBoard


posInf = 1000
negInf = -1000
moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]
enemy = getPlayerOne()


def reach(startPos, cLevel):
    """Returns a list of all possible positions for a worker"""
    moveReach, buildReach = [], []
    # Going through all adjacent spaces
    for op in moves:
        pos = newPosition(op, startPos)

        # Position in bounds, not occupied by worker and not already realised
        if pos not in workerLoc and not outBounds(pos) and pos not in buildReach and pos not in moveReach:
            buildReach.append(pos)
            if pos in buildLoc:
                bLevel = findBuildLevel(pos)

                if bLevel - 1 == cLevel or bLevel == cLevel or bLevel < cLevel:  # Can climb
                    moveReach.append(pos)

            else:  # Can move
                moveReach.append(pos)

    return moveReach, buildReach


def playMiniMax(pos, player):
    """Currently set to run minimax"""
    # Get evaluations for both workers
    evaluations = [runMiniMax(pos[0], 0, player), runMiniMax(pos[1], 1, player)]
    worker = 1

    if evaluations[0][1][0] > evaluations[1][1][0]:  # Find if worker C or D has the better option and switch if nesc.
        worker = 0

    # Current worker position and the new position to either move to or build on
    workerPos = pos[worker]
    newPos = evaluations[worker][1][1]

    if evaluations[worker][0] == "move":
        print("{} Moving to: {}".format(worker, newPos))
        pos[worker] = workerMove(player, workerPos, worker, newPos)
    else:
        print("{} Building on: {}".format(worker, newPos))
        workerBuild(newPos)

    # If moving will return the updated position otherwise pos does not change
    return pos


def runMiniMax(currentPos, refIndex, player):
    """Calls the minimax algorithm to evaluate options for both workers and then makes the highest ranked move"""
    moveEval = minimax(currentPos, 2, negInf, posInf, refIndex, True, True, player)
    buildEval = minimax(currentPos, 2, negInf, posInf, refIndex, False, True, player)

    print("Worker: {}, move: {} and build: {}".format(player[refIndex], moveEval, buildEval))

    if moveEval[0] > buildEval[0]:
        return "move", moveEval
    else:
        return "build", buildEval


def minimax(pos, depth, alpha, beta, refIndex, movement, maximising, player):
    """Pos is the position to be evaluated, depth is the number of nodes to test, alpha and beta are to track for
    pruning, activePlayer is the player reference and maxPlayer represents whether aiming to maximise or minimise.

    Movement represents working/climbing (0) or building (1)"""
    bestPos = []
    level = int(player[refIndex][3])
    workerLevels = int(player[0][3]), int(player[1][3])
    children = reach(pos, level)[movement]

    if depth == 0:  # Reached end of search

        if movement:
            return movementEvaluation(pos, children, workerLevels, refIndex), pos
        else:
            return buildEvaluation(pos, children, level), pos

    # Need to maximise
    if maximising:
        maxEval = negInf
        for child in children:
            # Recursive call for min search
            currentEval = minimax(child, depth - 1, alpha, beta, refIndex, movement, False, player)[0]

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

            minEval = min(minEval, currentEval)
            beta = min(beta, minEval)

            if beta <= alpha:
                break

        return minEval, bestPos


def calcLevelScore(level):
    match level:
        case 1:
            return 80
        case 2:
            return 200
        case 3:
            return 1000
        case _:
            return 0


def movementEvaluation(currentPos, currentReach, workerLevels, refIndex):
    """For a given possible position evaluate its effectiveness for movement"""
    levelScore, buildingScore, threatScore = 0, 0, 0
    if currentPos == [1, 1]:
        print(currentReach)

    # Get workers level
    workerLevel = workerLevels[refIndex]
    friend = friendIndex(refIndex)

    if currentPos in buildLoc:
        workerLevel = findBuildLevel(currentPos)

    if workerLevel != 0:
        # Add points depending upon workers current level
        levelScore += (calcLevelScore(workerLevel) + calcLevelScore(workerLevels[friend])
                       - (calcLevelScore([0]) + calcLevelScore([1])))

    # Points for surrounding buildings
    for pos in currentReach:
        if pos in buildLoc:
            buildLevel = findBuildLevel(pos)

            if workerLevel + 1 == buildLevel:
                buildingScore += 70
            elif workerLevel + 2 == buildLevel:
                buildingScore -= 50
            elif workerLevel + 3 == buildLevel:
                buildingScore -= 20
            else:
                buildingScore += 50

    # Win imminent
    if workerLevel == 3 and threatScore >= 2:
        threatScore = 2000

    print("Moving Pos: {}, Level: {}, Building: {}, Threat: {}".format(currentPos, levelScore, buildingScore, threatScore))

    # Building score the has the highest weighting
    return levelScore + buildingScore + threatScore


def buildEvaluation(currentPos, currentReach, workerLevel):
    """For a given possible position evaluate its effectiveness for building"""
    accessScore, enemyScore = 0, 0
    # Find the reachable positions of other workers on the board
    enemyAReach, enemyBReach = reach(workerLoc[0], enemy[3])[1], reach(workerLoc[1], enemy[4])[1]

    for pos in currentReach:
        if pos in enemyAReach or pos in enemyBReach:  # Negate points if building in reach of enemy
            enemyScore -= 10

        if pos in buildLoc:  # Points if a building reachable
            buildLevel = findBuildLevel(pos)

            if buildLevel == workerLevel:
                accessScore += 200
            elif buildLevel + 1 == workerLevel:
                accessScore += 30
            elif buildLevel + 2 == workerLevel:
                accessScore += 15
            else:
                accessScore += 5

    print("Build Pos: {}, Access: {}, Enemy: {}".format(currentPos, accessScore, enemyScore))

    # Access score has the highest weighting
    return accessScore + enemyScore


def friendIndex(refIndex):
    if refIndex == 1:
        return 0
    else:
        return 1
