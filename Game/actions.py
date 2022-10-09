"""
This file enables players to perform actions (moving, climbing and building) with their workers.
"""
from Misc.exceptions import BoundsError, SelectionError, SpaceTakenError

board = [["|    |" for a in range(5)] for b in range(5)]  # Build the board
workerLoc = []  # Track the worker locations

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

        if getLevelFromBoard(newPos) > 0:  # If space needs to be climbed
            buildingLevel = getLevelFromBoard(newPos)
            workerLevel = player[levelIndex]

            if 0 < workerLevel > buildingLevel:
                player[levelIndex] -= 1
                updateRef(pRef, player, refIndex, levelIndex)
                board[startPos[0]][startPos[1]] = buildCode[getLevelFromBoard(startPos)]

            elif buildingLevel == workerLevel:  # Traversing same level buildings
                board[startPos[0]][startPos[1]] = buildCode[int(buildingLevel)]

            elif (buildingLevel - 1) == workerLevel:  # Going up a level
                # Updating worker level
                player[levelIndex] += 1
                updateRef(pRef, player, refIndex, levelIndex)

                if buildingLevel > 1:  # If higher than L1 need to replace old building
                    board[startPos[0]][startPos[1]] = buildCode[buildingLevel - 1]
                else:  # No building occupied so old space needs to be cleared
                    clearPos(startPos)
            else:
                raise BoundsError

        elif getLevelFromBoard(startPos) > 0:  # Player descending
            board[startPos[0]][startPos[1]] = buildCode[player[levelIndex]]  # Update the board
            player[levelIndex] -= 1

            if getLevelFromBoard(startPos) > 1:
                player[levelIndex] = 0

            # Update the worker details and icon
            updateRef(pRef, player, refIndex, levelIndex)

        else:
            clearPos(startPos)

        workerLoc[workerLoc.index(startPos)] = newPos  # Update worker location in location tracker
        board[newPos[0]][newPos[1]] = player[refIndex]  # Update player position on the board

        return [newPos[0], newPos[1]]


def workerBuild(buildPos):
    """
    Given a position either register a new building or increase the height of the present building

    :param buildPos: The position in which the building is being built
    """
    if buildPos in workerLoc:  # Space is taken by a worker
        raise SelectionError
    elif getLevelFromBoard(buildPos) == 0:  # Space not built on so know it's the first level
        newLevel = buildCode[1]

    else:  # Building higher than l1
        if maxHeight(buildPos):
            raise SelectionError

        newLevel = buildCode[getLevelFromBoard(buildPos) + 1]

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
        return pRef, 3
    else:
        return pRef, 4


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
    Standardise a worker reference

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


def getLevelFromBoard(pos):
    """
    Get the level of a given position

    :param pos: Position to retrieve the level of
    :return: The level of the position
    """
    boardValue = board[pos[0]][pos[1]]
    if boardValue[3].isdigit():
        return int(boardValue[3])
    else:
        return 0
