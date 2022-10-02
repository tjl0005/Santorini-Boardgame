"""
This file contains an implementation of a greedy AI with some enhancements to ensure a more complex competition
Originally implemented to test and tune the minimax AI, it can be used as an easy competitor.
"""
from Game.options import workerMove, newPosition, buildLoc, findBuildLevel, workerBuild, workerLoc, outBounds, maxHeight
from Game.ui import displayBoard


def easyAI(startPos, player):
    """
    Use factors of the current positions surroundings to decide the next best move, uses a greedy approach
    :param startPos: The initial positions of both workers
    :param player: The players whose move it is
    :return: The updated starting positions
    """
    highest = getHighest()

    xLevel, yLevel = int(player[0][3]), int(player[1][3])
    xEvaluation = evaluateOptions(highest, startPos[0], xLevel, 1)
    yEvaluation = evaluateOptions(highest, startPos[1], yLevel, 0)

    if xEvaluation[1] == 0 and yEvaluation[1] == 0:
        print("\nPlayer {}, has lost!!".format(player[2]))
        exit()
    elif xEvaluation[1] > yEvaluation[1]:
        if xEvaluation[0]:
            print("{} moving to {}".format(player[0], xEvaluation[2]))
            startPos[0] = workerMove(player, startPos[0], 0, xEvaluation[2])
        else:
            print("{} building on {}".format(player[0], xEvaluation[2]))
            workerBuild(xEvaluation[2])
    else:
        if yEvaluation[0]:
            print("{} moving to {}".format(player[1], yEvaluation[2]))
            startPos[1] = workerMove(player, startPos[1], 1, yEvaluation[2])
        else:
            print("{} moving to {}".format(player[1], yEvaluation[2]))
            workerBuild(yEvaluation[2])

    displayBoard()
    return startPos


def evaluateOptions(highest, startPos, cLevel, friendIndex):
    """
    Given a starting position attempt to find the best position and give it a score
    :param highest: A list containing the current highest buildings, if there are no buildings it is an empty list
    :param startPos: The starting position of the current worker
    :param cLevel: The level of the current worker
    :param friendIndex: The index representing the friend to the current worker
    :return: A list containing a flag (Move or Build), a score and the new position
    """
    if not highest:  # There are no higher buildings so build one
        return [False, 10, bestBuild(startPos, canReach(startPos, highest, cLevel, "move"), friendIndex)]

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
    """
    Get the highest buildings currently on the board
    :return: A list containing the highest buildings and their level
    """
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
    """
    Take either a worker or building reference and only return the level
    :param ref: The reference to the building or worker
    :return: Integer representing the current level
    """
    return ref.replace("|", "").replace(" ", "").replace("L", "").replace("C", "").replace("D", "")


def bestBuild(startPos, reach, friendIndex):
    """
    Find the best position to be built on
    :param startPos: The current workers position
    :param reach: The building reach of the worker
    :param friendIndex: The index of the current workers friend
    :return: The best position to build in
    """
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
    """
    Evaluate the current buildings around the worker and return the best position to either climb or build on
    :param highest: A list containing the highest buildings
    :param cLevel: The current workers level
    :param startPos: The current workers initial position
    :param friendIndex: The index of the workers friend
    :return: A flag (Climb or build) and the new position to perform that action on
    """
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
        return True, buildSame[0]
    elif buildNew:  # No available buildings, so build new one
        return True, bestBuild(startPos, canReach(startPos, highest, cLevel, "build"), friendIndex)
    else:  # No position to build or move to
        return True, getBest(highest, reachable)


def canReach(startPos, highest, cLevel, movement):
    """
    Given a movement type (Climb or build) return a list of all possible positions the given action can be done for
    :param startPos: The workers initial position
    :param highest: The current highest buildings on the board
    :param cLevel: The current workers level
    :param movement: A flag representing either Climb (True) or Build (False)
    :return: The current reach of the worker
    """
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
    """
    A last resort to find the best position to move to given access to buildings
    :param highest: List of the highest buildings on the board
    :param reachable: Current reach of the selected worker
    :return: Either the best position to move to or nothing
    """
    best = []

    for pos in reachable:
        posReach = len(canReach(pos, highest, highest[1], "climb"))  # Each reachable buildings counts as a point

        if pos in buildLoc:  # Being able to climb selected pos adds values
            posReach += 1

        best.append(posReach)

    if len(best) > 1:
        return reachable[best.index(max(best))]


def getSpaceAround(currentPos, friendPos, reach):
    """
    If a building cannot be reached via WASD directions attempt to use WA, WD, SA an SD
    :param currentPos: Current position of the worker
    :param friendPos: Current position of the workers friend
    :param reach: Current move reach of the worker
    :return: The next best position
    """
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
    """
    Given the starting and target positions get the direction required to move to or towards the target
    :param startPos: The initial position of the worker
    :param targetPos: The desired position of the worker
    :return: A string representing the relevant direction
    """
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
    """
    Give the location of the workers friend
    :param index: Current workers index
    :return: The friends location
    """
    if index == 0:
        return workerLoc[3]
    else:
        return workerLoc[2]
