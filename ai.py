from game import newPosition, findBuildLevel, findWorkerLevel, getWorkerLoc, getBuildDetails, getBuildLoc, workerMove, \
    workerBuild

# Added ability to determine direction
# Function to select best positions on the board
# Skeleton of basic AI to compete against

moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]


def getPossibleMoves(startPos, active, player, workerLoc, buildLoc):
    """Find all potential moves for a specified worker"""
    move, build, climb, descend = [], [], [], []

    for op in moves:
        pos = newPosition(op, startPos)

        if pos not in workerLoc and not any(0 < val > 4 for val in pos):  # Looking for valid spaces
            build.append(pos)  # Can build anywhere in bounds and without a worker

            if pos not in buildLoc:  # Empty space
                move.append(pos)

            else:  # Space has a building in it
                bLevel = findBuildLevel(pos)
                wLevel = findWorkerLevel(player, active)[2]

                if bLevel > player[wLevel]:  # Can climb it
                    climb.append(pos)
                else:  # Can only descend
                    descend.append(pos)

        return move, build, climb, descend


def getDirection(startPos, newPos):
    startX, startY = startPos[0], startPos[1]  # Left/Right
    newX, newY = newPos[0], newPos[1]  # Up/Down

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


def getHighest():
    """Returns all the highest buildings currently on the board"""
    highest = []
    buildDetails = getBuildDetails()

    for build in buildDetails:
        build = [build[0], build[1].replace("|", "").replace(" ", "").replace("L", "")]  # Standardise reference

        if not highest:  # First building so automatically the highest
            highest = [build]

        else:
            for i in range(len(highest)):
                int(highest[i][1].replace("|", "").replace(" ", "").replace("L", ""))

                if highest[i][1] < build[1]:  # New building higher level so replace old records
                    highest = [build]

                elif highest[i][1] == build[1]:  # New building same level so append
                    highest.append(build)

    return highest


def getBest(highest, reachable):
    """Receives all possible moves and needs to select which position is the best to be in"""
    best = []
    bLevel = int(highest[0][1].replace("|", "").replace(" ", "").replace("L", ""))

    print("Reachable: {}".format(reachable))

    for pos in reachable:
        posReach = canReach(pos, highest, bLevel, "climb")
        best.append(len(posReach))

    best = best.index(max(best))

    # What if a connecting building connects to others?

    return reachable[best]


def canReach(startPos, highest, cLevel, movement):
    reach = []
    match = []
    workerLoc = getWorkerLoc()
    buildLoc = getBuildLoc()

    # Going through all adjacent spaces
    for op in moves:
        pos = newPosition(op, startPos)

        # Position in bounds and empty
        if pos not in workerLoc and not any(0 < val > 4 for val in pos):
            if pos in buildLoc and movement == "climb":
                bLevel = findBuildLevel(pos)
                if bLevel - 1 == cLevel:
                    print("Found space to climb")
                    reach.append(pos)
                elif bLevel == cLevel:
                    print("Found space to cross")
                    reach.append(pos)
                elif bLevel < cLevel:
                    print("Found space to descend from")
                    reach.append(pos)

                # Find match
                for val in highest:
                    if val[0] in reach:
                        match.append(val[0])

            elif pos not in buildLoc and movement == "move":
                print("Found position to move to")
                match.append(pos)

    return match


def bestBuild(startPos, reach):
    # Attempt to build towards friend worker
    friend = getDirection(startPos, getWorkerLoc()[3])
    friendDir = newPosition(friend, startPos)

    if friendDir in reach:
        print("Can build towards friend")
        workerBuild(friendDir)
    else:
        print("Cannot build towards other worker so building in next space")
        workerBuild(reach[0])


def basicAI(startPos, player):
    highest = getHighest()
    hLevel = int(highest[0][1])
    cLevel = player[3]  # Worker level for C

    if not highest:  # There are no higher buildings
        bestBuild(startPos, canReach(startPos, highest, cLevel, "move"))

    elif hLevel != cLevel:  # Can move to higher buildings
        if len(highest) > 1:  # There's a few higher buildings so need to find which can be reached
            print("Need to select closest one")
            reachable = canReach(startPos, highest, cLevel, "climb")
            getBest(highest, reachable)  # Use near positions to find which is most profitable
            direction = getDirection(startPos, getBest(highest, reachable))

            workerMove(player, startPos, 0, newPosition(direction, startPos))

        else:  # Only 1 building that needs to be moved towards
            direction = getDirection(startPos, highest[0][0])  # Move in this direction
            movePos = newPosition(direction, startPos)

            # Check if AI can move in direction of building, build a new one nearby
            if movePos not in getWorkerLoc():
                workerMove(player, startPos, 0, movePos)
            else:
                bestBuild(startPos, canReach(startPos, highest, cLevel, "move"))

    else:  # Already at the highest level
        print("On highest level")
        options = []
        for op in highest:
            if op not in getWorkerLoc() and not any(0 < val > 4 for val in op):  # Looking for valid spaces
                print("Can build nearby")
            else:
                options.append(op)
                print("Making list of unreachable buildings")

        if options:
            print("Need to get closest building to move towards")

    print("AND NOW AI HAS ENDED")


def minimax():
    return


def beam():
    return


def monte():
    return
