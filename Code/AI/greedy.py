from Code.Game.playOptions import workerMove, newPosition, buildLoc, findBuildLevel, workerBuild, workerLoc, outBounds, maxHeight
from Code.Game.ui import displayBoard


def easyAI(startPos, player):
    """Uses factors of the current selected workers position to select a good move, not great, just okay really"""
    displayBoard()
    highest = getHighest()

    xLevel, yLevel = int(player[0][3]), int(player[1][3])
    xEvaluation = evaluateOptions(highest, startPos[0], xLevel, 1)
    yEvaluation = evaluateOptions(highest, startPos[1], yLevel, 0)

    if xEvaluation[1] == 0 and yEvaluation[1] == 0:
        print("\nPlayer {}, has lost!!".format(player[2]))
        exit()
    elif xEvaluation[1] > yEvaluation[1]:
        if xEvaluation[0]:
            startPos[0] = workerMove(player, startPos[0], 0, xEvaluation[2])
        else:
            workerBuild(xEvaluation[2])
    else:
        if yEvaluation[0]:
            startPos[1] = workerMove(player, startPos[1], 1, yEvaluation[2])
        else:
            workerBuild(yEvaluation[2])

    return startPos


def evaluateOptions(highest, startPos, cLevel, friendIndex):
    if not highest:  # There are no higher buildings so build one
        return [False, 0, bestBuild(startPos, canReach(startPos, highest, cLevel, "move"), friendIndex)]

    # Can move to higher buildings
    elif int(highest[1]) != cLevel:
        # There's a few higher buildings so need to find which can be reached
        if len(highest) > 1:
            newPos = canBuild(highest, cLevel, startPos, friendIndex)
            if not newPos[0]:
                return [True, 15, newPos[1]]
            else:
                return [False, 15, newPos[1]]

        # Only 1 building that needs to be moved towards
        else:
            direction = getDirection(startPos, highest[0])  # Move in this direction
            movePos = newPosition(direction, startPos)

            if movePos not in workerLoc and int(highest[1]) - 1 == cLevel:
                return [True, 25, movePos]

            else:
                return [False, 20, canBuild(highest, cLevel, startPos, friendIndex)[1]]

    else:  # Already at the highest level
        newPos = canBuild(highest, cLevel, startPos, friendIndex)
        if newPos[0]:
            return [False, 30, newPos[1]]
        else:
            return [False, 30, newPos]


def getHighest():
    """Returns all the highest buildings currently on the board"""
    highest = []

    if not buildLoc:
        return

    for build in buildLoc:
        if not maxHeight(build):  # Not a valid building
            level = findBuildLevel(build)
            if not highest:  # First building to be checked so automatically the highest
                highest = [build, level]
            else:
                for i in range(len(buildLoc) - 1):  # Already checked first building
                    if build != highest[0] and highest[1] < level:  # New building higher level so replace
                        highest = [build, level]

                    elif highest[1] == level and highest[0] != build:  # New building same level so append
                        highest.append(build)
    return highest


def stdRef(ref):
    """Takes either a worker or building reference and only returns the letter or number"""
    return ref.replace("|", "").replace(" ", "").replace("L", "").replace("C", "").replace("D", "")


def bestBuild(startPos, reach, friendIndex):
    """Attempts to find the best position to build in for a selected worker"""
    for build in buildLoc:  # First check if a nearby building can be used
        if build in reach and not maxHeight(build):
            return build

    # Attempt to build towards friend worker
    friendPos = friendLoc(friendIndex)

    if friendPos in reach:
        return friendPos
    else:
        spaceAround = getSpaceAround(startPos, friendPos, reach)
        if spaceAround:  # Build near friend
            return spaceAround
        else:  # Cannot build towards other worker so next available space
            return reach[0]


def canBuild(highest, cLevel, startPos, friendIndex):
    """Makes best building decision"""
    reachable = canReach(startPos, highest, cLevel, "build")
    buildSame = []
    buildNew = []

    # Going to climb or build
    for pos in reachable:
        # Know there is a building to check
        if pos in buildLoc:
            bLevel = findBuildLevel(pos)
            # If worker can climb higher promise that
            if bLevel > cLevel:  # Building higher so climbing it
                return False, newPosition(getDirection(startPos, pos), startPos)

            # Opportunity for worker to build on top of another building
            elif bLevel == cLevel:
                buildSame.append(pos)

        # Worker has to build new
        elif pos not in workerLoc:
            buildNew.append(pos)

    # Shows priority of opportunities
    if buildSame:  # Building same level so building on it
        if len(buildSame) > 1:
            return True, buildSame
        else:
            return True, buildSame[0]
    elif buildNew:  # No available buildings, so build new one
        return True, bestBuild(startPos, canReach(startPos, highest, cLevel, "build"), friendIndex)
    else:  # No position to build or move to
        return True, getBest(highest, reachable)


def canReach(startPos, highest, cLevel, movement):
    """Returns a list of all possible positions for a worker"""
    reach, match = [], []
    # Going through all adjacent spaces
    for op in ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]:
        pos = newPosition(op, startPos)

        # Position in bounds, not occupied by worker and not already realised
        if pos not in workerLoc and not outBounds(pos) and not maxHeight(pos) and pos not in reach:
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
    if len(match) > 1:
        return match
    else:
        return match[0]


def getBest(highest, reachable):
    """Receives all possible moves and needs to select which position is the best to be in"""
    best = []

    for pos in reachable:
        posReach = len(canReach(pos, highest, highest[1], "climb"))  # Each reachable buildings counts as a point

        if pos in buildLoc:  # Being able to climb selected pos adds values
            posReach += 1

        best.append(posReach)

    if len(best) > 1:
        return reachable[best.index(max(best))]
    else:
        return


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
        return workerLoc[3]
    else:
        return workerLoc[2]
