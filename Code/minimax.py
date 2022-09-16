from game import newPosition, workerMove, workerBuild, findBuildLevel, outBounds, workerLoc, buildLoc, moves
from ui import displayBoard

posInf = 1000
negInf = -1000


def reach(startPos, workerLevel):
    """Find potential move and build options for a specified worker"""
    move, build = [], []

    for op in moves:
        pos = newPosition(op, startPos)

        # Looking for valid spaces
        if pos not in workerLoc and not outBounds(pos):
            build.append(pos)  # Can build anywhere in bounds and without a worker

            if pos not in buildLoc or findBuildLevel(pos) > workerLevel:  # Can move/climb
                move.append(pos)

    return move, build


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
        print("Moving to: {}".format(newPos))
        pos[worker] = workerMove(player, workerPos, worker, newPos)
    else:
        print("Building on: {}".format(newPos))
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
    level = int(player[refIndex][3])

    if depth == 0:  # Reached end of search

        if movement:
            # print(player[refIndex])
            return movementEvaluation(pos, level), pos
        else:
            # print(player[refIndex])
            return buildEvaluation(pos, level), pos

    children = reach(pos, level)[movement]
    bestPos = []

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

        if pos in buildLoc:
            buildLevel = findBuildLevel(pos)

            if workerLevel == buildLevel:
                buildingScore += 5
            else:
                threatScore += 1
                if workerLevel + 1 == buildLevel:
                    buildingScore += 80
                elif workerLevel + 2 == buildLevel:
                    buildingScore -= 50
                elif workerLevel + 3 == buildLevel:
                    buildingScore -= 20

    # Near win imminent
    if workerLevel == 2 and threatScore >= 2:
        threatScore = 2000

    # Building score the has the highest weighting
    return levelScore + 1.5 * buildingScore + threatScore


def buildEvaluation(position, workerLevel):
    """For a given possible position evaluate its effectiveness for building"""
    accessScore, enemyScore, friendScore = 0, 0, 0

    # Find the reachable positions of other workers on the board
    enemyAReach, enemyBReach = reach(workerLoc[0], workerLevel)[1], reach(workerLoc[1], workerLevel)[1]
    friendReach = []

    # Find friend location
    for loc in workerLoc[-2:]:
        if loc != position:
            friendReach = reach(loc, workerLevel)[1]

    for op in moves:
        pos = newPosition(op, position)

        if pos in enemyAReach or pos in enemyBReach:  # Negate points if building in reach of enemy
            enemyScore -= 10
        elif pos in friendReach:  # Points if building in reach of friend worker
            enemyScore += 10

        if pos in buildLoc:  # Points if a building reachable
            buildLevel = findBuildLevel(pos)

            if buildLevel == workerLevel:
                accessScore += 60
            elif buildLevel + 1 == workerLevel:
                accessScore += 30
            elif buildLevel + 2 == workerLevel:
                accessScore += 15

    # Access score has the highest weighting
    return 1.5 * accessScore + enemyScore + friendScore
