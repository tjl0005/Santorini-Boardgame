"""
This file enables players to perform actions (moving, climbing and building) with their workers.
"""
from Misc.exceptions import BoundsError, SelectionError, SpaceTakenError

# Build board
board = [["|    |" for a in range(5)] for b in range(5)]
workerLoc, buildLoc = [], []

# Dictionary to get the label for a specified build level
buildCode = {
    1: "| L1 |",
    2: "| L2 |",
    3: "| L3 |",
    4: "| {} |"
}


def workerMove(player, startPos, refIndex, newPos):
    """
    Given a new position move the selected worker to that position. This movement will be validated before the board is
    updated.
    :param player: The player to perform the action for
    :param startPos: A list containing the starting positions of players workers in format of [[0, 0], [1, 1]]
    :param refIndex The workers reference index
    :param newPos The position to move to
    :return: A list containing the new current positions
    """
    if newPos in [5, -1]:  # Player attempting to go out of bounds
        print("Fault 3")
        raise BoundsError
    elif newPos in workerLoc:  # Space in use by another player
        print("Fault 4")
        raise SpaceTakenError
    else:  # Standard movement
        pRef, levelIndex = findLevelIndex(player[refIndex])

        if newPos in buildLoc:  # Check if space can be climbed and how so
            climb = workerClimb(newPos, player[levelIndex])

            if not climb[0]:  # Cannot climb
                raise BoundsError

            elif type(climb[1]) is str:  # Descending or moving between buildings on same level
                if climb[1] == "desc":
                    player[levelIndex] -= 1
                    updateRef(pRef, player, refIndex, levelIndex)
                    board[startPos[0]][startPos[1]] = buildCode[findBuildLevel(startPos)]
                else:
                    board[startPos[0]][startPos[1]] = buildCode[int(climb[1])]

            else:  # Going up a level
                player[levelIndex] += 1  # Update worker level
                updateRef(pRef, player, refIndex, levelIndex)

                if climb[1] > 1:  # If higher than L1 need to replace old building
                    board[startPos[0]][startPos[1]] = buildCode[climb[1] - 1]
                else:  # No building occupied so a blanks space
                    clearPos(startPos)

        elif startPos in buildLoc:  # Player descending
            board[startPos[0]][startPos[1]] = buildCode[player[levelIndex]]  # Update the board
            player[levelIndex] -= 1

            if findBuildLevel(startPos) > 1:
                player[levelIndex] = 0

            # Update the worker details and icon
            updateRef(pRef, player, refIndex, levelIndex)

        else:
            clearPos(startPos)

        workerLoc[workerLoc.index(startPos)] = newPos
        board[newPos[0]][newPos[1]] = player[refIndex]  # Update player position on the board

        return [newPos[0], newPos[1]]


def workerClimb(climbPos, workerLevel):
    """
    Given a new position check if the worker is required to climb the building. If there is no building it is seen as a
    standard movement, otherwise the worker can either go up, across or down buildings.
    :param climbPos: The position on the board to be tested
    :param workerLevel: The current workers level
    :return:
    """
    buildingLevel = findBuildLevel(climbPos)

    if (buildingLevel - 1) == workerLevel:  # Worker is going to climb up one level
        return True, buildingLevel

    elif buildingLevel == workerLevel:  # Worker going across buildings
        return True, str(buildingLevel)

    elif 0 < workerLevel > buildingLevel:  # Worker is descending
        return True, "desc"

    else:  # Standard movement detection
        return False, ""


def workerBuild(buildPos):
    """
    Given a position either register a new building or increase the height of the present building
    :param buildPos: The position in which the building is being built
    """
    if buildPos in workerLoc:  # Space is taken by a worker
        raise SelectionError
    elif buildPos not in buildLoc:  # Space not built on so know it's the first level
        newLevel = buildCode[1]
        buildLoc.append(buildPos)  # Store building position in taken locations to avoid collisions

    else:  # Building higher than l1
        if maxHeight(buildPos):
            raise SelectionError

        newLevel = buildCode[findBuildLevel(buildPos) + 1]

    board[buildPos[0]][buildPos[1]] = newLevel  # Update the board with new building position


def newPosition(direction, pos):
    """
    Calculate a new position on the board using the desired direction and the initial position
    :param direction: The direction to move in (W, A, S, D, WA, WD, SA and SD)
    :param pos: The initial position
    :return: The new position
    """
    newPos = pos[:]  # Making a copy

    match direction:
        case "W":
            newPos[0] -= 1
        case "A":
            newPos[1] -= 1
        case "S":
            newPos[0] += 1
        case "D":
            newPos[1] += 1
        case "WA":
            newPos[0] -= 1
            newPos[1] -= 1
        case "WD":
            newPos[0] -= 1
            newPos[1] += 1
        case "SA":
            newPos[0] += 1
            newPos[1] -= 1
        case "SD":
            newPos[0] += 1
            newPos[1] += 1
        case _:
            print("Fault 8")
            raise SelectionError()

    return newPos


def findLevelIndex(pRef):
    """
    Given a player reference return the worker tag and level index, as wll as the standardised reference
    :param pRef: The worker reference
    :return: Standardised worker reference and the level index
    """
    pRef = stdRef(pRef)
    pRef = removeLevel(pRef)

    if pRef in ["A", "C"]:
        k, j = 0, 3
    else:
        k, j = 1, 4

    # Reference to the worker, worker tag and level index
    return pRef, j


def findBuildLevel(buildPos):
    """
    Given a position on the board where a building is present return the level of that building
    :param buildPos: Position of the building in question
    :return: The build level
    """
    buildRef = board[buildPos[0]][buildPos[1]]
    return int(buildRef[3])


def updateRef(pRef, player, refIndex, levelIndex):
    """
    Standardise a player reference
    :param pRef: The worker reference
    :param player: The current player
    :param refIndex: The workers index reference
    :param levelIndex: The workers level reference
    """
    player[refIndex] = "| {}{} |".format(removeLevel(stdRef(pRef)), player[levelIndex])  # Update worker reference
    if player[levelIndex] == 3:
        print("\nWow! Player {}, has won!".format(player[2]))
        exit()


def stdRef(ref):
    """
    Standardise a worker reference e.g. A
    :param ref: The reference to be standardised
    :return: The single character reference
    """
    return ref.replace("|", "").replace(" ", "").replace("L", "")


def removeLevel(ref):
    """
    Return the given reference without numbers
    :param ref: The worker reference
    :return: Worker reference without a number
    """
    return ''.join([i for i in ref if not i.isdigit()])


def clearPos(startPos):
    """
    Clear the given position from the board
    :param startPos: The position which is now blank
    """
    board[startPos[0]][startPos[1]] = "|    |"  # Clear icon from old position


def maxHeight(buildPos):
    """
    Check if a building is already at the max height (Dome, {})
    :param buildPos: The tested buildings position
    :return: True if the building is at the max height, otherwise nothing
    """
    if board[buildPos[0]][buildPos[1]] == "| {} |":
        return True


def outBounds(pos):
    """
    Check if a given position is within bounds of the board (0,0 to 4,4)
    :param pos: The tested position
    :return: True if within bounds, otherwise nothing
    """
    if any(0 > val for val in pos) or any(val > 4 for val in pos):
        return True
