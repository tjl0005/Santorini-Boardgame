from ai import possiblePositions
from game import newPosition, findBuildLevel, getWorkerLoc, getBuildDetails, getBuildLoc, workerMove, workerBuild, \
    getMoves, board
from ui import displayBoard
# Not in a great state but helped to understand


def bot(startPos, player, levelIndex, refIndex):
    """Uses factors of the current selected workers position to select a good move, not great, just okay really"""
    print("Starting in AI: {}".format(startPos))
    highest = getHighest()
    cLevel = int(stdRef(player[levelIndex]))

    print("Can move: {}".format(possiblePositions(startPos, player[refIndex])))

    if not highest:  # There are no higher buildings so build one
        bestBuild(startPos, canReach(startPos, highest, cLevel, "move"), levelIndex)

    # Can move to higher buildings
    elif int(highest[0][1]) != cLevel:
        # There's a few higher buildings so need to find which can be reached
        if len(highest) > 1:
            print("Need to select closest one")
            pos = canBuild(highest, cLevel, startPos, levelIndex)

            if pos != startPos:
                return workerMove(player, startPos, refIndex, pos)

        # Only 1 building that needs to be moved towards
        else:
            print("Attempting to move towards highest building")
            direction = getDirection(startPos, highest[0][0])  # Move in this direction

            movePos = newPosition(direction, startPos)

            if movePos not in getWorkerLoc() and int(highest[0][1]) - 1 == cLevel:
                print("Moving towards direction of highest building")
                return workerMove(player, startPos, refIndex, movePos)
            else:
                print("Building towards highest building")
                canBuild(highest, cLevel, startPos, levelIndex)

    else:  # Already at the highest level
        print("On highest level")
        pos = canBuild(highest, cLevel, startPos, levelIndex)
        if pos != startPos:
            return workerMove(player, startPos, refIndex, pos)

    print("Ending in AI: {}".format(startPos))
    displayBoard(board)
    return startPos


def getHighest():
    """Returns all the highest buildings currently on the board"""
    highest = []
    buildDetails = getBuildDetails()

    if not buildDetails:
        return

    for build in buildDetails:
        build = [build[0], stdRef(build[1])]  # Standardise reference

        if build[1] != "{}":  # Not a valid building
            if not highest:  # First building to be checked so automatically the highest
                highest = [build]
            else:
                for i in range(len(buildDetails) - 1):  # Already checked first building
                    if highest[0][1] < build[1] and highest[0][0] != build[0]:  # New building higher level so replace
                        highest = [build]

                    elif highest[0][1] == build[1] and highest[0][0] != build[0]:  # New building same level so append
                        highest.append(build)

    return highest


def stdRef(ref):
    """Takes either a worker or building reference and only returns the letter or number"""
    return ref.replace("|", "").replace(" ", "").replace("L", "").replace("C", "").replace("D", "")


def bestBuild(startPos, reach, workerIndex):
    """Attempts to find the best position to build in for a selected worker"""
    for build in getBuildDetails():  # First check if a nearby building can be used
        if build[0] in reach and build[1] != "| () |":
            print("Building nearby: {}".format(build[0]))
            return workerBuild(build[0])

    # Attempt to build towards friend worker
    friendPos = friendLoc(workerIndex)

    if friendPos in reach:
        print("Can build towards friend space")
        workerBuild(friendPos)
    else:
        spaceAround = getSpaceAround(startPos, friendPos, reach)
        print("Building near friend: {}".format(spaceAround))
        if spaceAround:
            workerBuild(spaceAround)
        else:
            print("Cannot build towards other worker so building in next space")
            workerBuild(reach[0])


def canBuild(highest, cLevel, startPos, workerIndex):
    """Makes best building decision"""
    reachable = canReach(startPos, highest, cLevel, "build")
    buildSame = []
    buildNew = []

    # Going to climb or build
    for pos in reachable:
        # Know there is a building to check
        if pos in getBuildLoc():
            bLevel = findBuildLevel(pos)
            # If worker can climb higher promise that
            if bLevel > cLevel:
                print("Building higher so climbing: {}".format(pos))
                return newPosition(getDirection(startPos, pos), startPos)

            # Opportunity for worker to build on top of another building
            elif bLevel == cLevel:
                buildSame.append(pos)

        # Worker has to build new
        elif pos not in getWorkerLoc():
            buildNew.append(pos)

    # Shows priority of opportunities
    if buildSame:
        print("Building same level so building on it")
        workerBuild(buildSame[0])
    elif buildNew:
        print("No available buildings so building new one")
        bestBuild(startPos, canReach(startPos, highest, cLevel, "build"), workerIndex)
    else:
        print("No position to build or move to")
        # No position to build or move to
        return getBest(highest, reachable)

    return startPos


def canReach(startPos, highest, cLevel, movement):
    """Returns a list of all possible positions for a worker"""
    reach, match = [], []
    workerLoc, buildLoc = getWorkerLoc(), getBuildLoc()
    # Going through all adjacent spaces
    for op in getMoves():
        pos = newPosition(op, startPos)

        # Position in bounds, not occupied by worker and not already realised
        if pos not in workerLoc and not any(0 > val for val in pos) and not any(val > 4 for val in pos) and pos not in reach:
            # print("Moving: {}, Pos: {}".format(op, pos))
            if pos in buildLoc and movement == "climb":
                bLevel = findBuildLevel(pos)

                if bLevel - 1 == cLevel or bLevel == cLevel or bLevel < cLevel:
                    reach.append(pos)

                for val in highest:
                    if val[0] in reach:
                        match.append(val[0])

            elif pos not in buildLoc and movement == "move":
                match.append(pos)

            else:  # If wanting to build, can build at any level as long as no worker
                match.append(pos)

    return match


def getBest(highest, reachable):
    """Receives all possible moves and needs to select which position is the best to be in"""
    best = []
    bLevel = int(stdRef(highest[0][1]))

    for pos in reachable:
        posReach = len(canReach(pos, highest, bLevel, "climb"))  # Each reachable buildings counts as a point

        if pos in getBuildLoc():  # Being able to climb selected pos adds values
            posReach += 1

        best.append(posReach)

    best = best.index(max(best))  # Select the reachable position with the highest score

    return reachable[best]


def getSpaceAround(currentPos, friendPos, reach):
    """If a building cannot be built towards via WASD directions try diagonal directions"""
    if currentPos[0] == friendPos[0] or currentPos[1] == friendPos[1]:  # On same row or in same column
        abovePos = [friendPos[0] + 1, friendPos[1]]
        belowPos = [friendPos[0] - 1, friendPos[1]]

        leftPos = [friendPos[0], friendPos[1] + 1]
        rightPos = [friendPos[0], friendPos[1] - 1]

    else:  # Do not share a row or column
        abovePos = [currentPos[1] - 1, currentPos[1] - 1]
        belowPos = [currentPos[1] - 1, currentPos[1] + 1]

        leftPos = [currentPos[0] + 1, currentPos[0] - 1]
        rightPos = [currentPos[0] + 1, currentPos[0] + 1]

    # Return applicable position, no preference of order
    if abovePos in reach:
        return abovePos
    elif belowPos in reach:
        return belowPos
    elif leftPos in reach:
        return leftPos
    elif rightPos in reach:
        return rightPos


def getDirection(startPos, targetPos):
    """Given a starting position and target position, this will return the direction that must be travelled in"""
    startX, startY = startPos[0], startPos[1]  # Left/Right
    newX, newY = targetPos[0], targetPos[1]  # Up/Down

    xChange = startX - newX
    yChange = startY - newY

    if xChange == 0 and yChange >= 1:
        return "A"
    elif xChange == 0 and yChange <= -1:
        return "D"
    elif yChange == 0 and xChange >= 1:
        return "W"
    elif yChange == 0 and xChange <= -1:
        return "S"
    elif xChange >= 1 and yChange >= 1:
        return "WA"
    elif xChange >= 1 and yChange <= -1:
        return "WD"
    elif xChange <= -1 and yChange <= -1:
        return "SD"
    elif xChange <= -1 and yChange >= 1:
        return "SA"


def friendLoc(index):
    """Returns the location of the other, unselected, worker"""
    if index == 0:
        return getWorkerLoc()[3]
    else:
        return getWorkerLoc()[2]
