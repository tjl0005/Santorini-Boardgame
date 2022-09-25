from exceptions import SelectionError, BoundsError, SpaceTakenError

workerLoc = []
buildLoc = []
buildDetails = []

# Dictionary to get the label for a specified build level
buildCode = {
    1: "| L1 |",
    2: "| L2 |",
    3: "| L3 |",
    4: "| {} |"
}

# Generate board
board = [["|    |" for a in range(5)] for b in range(5)]


def workerMove(player, startPos, refIndex, newPos):
    """Complete task of moving the player on the board and detecting if selected movement requires a worker to climb
    or descend"""

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

            elif type(climb[1]) is str:  # Moving between buildings on same level
                if climb[1] == "desc":
                    player[levelIndex] -= 1
                    updateRef(pRef, player, refIndex, levelIndex)

                    currentLevel = findBuildLevel(startPos)
                    board[startPos[0]][startPos[1]] = buildCode[currentLevel]
                else:
                    board[startPos[0]][startPos[1]] = buildCode[int(climb[1])]

            else:  # Going up a level
                player[levelIndex] += 1  # Update worker level
                updateRef(pRef, player, refIndex, levelIndex)

                if climb[1] > 1:  # If higher than L1 need to replace old building
                    board[startPos[0]][startPos[1]] = buildCode[climb[1] - 1]
                else:  # No building occupied so a blanks space
                    clearPos(startPos)

        elif startPos in buildLoc:  # Player descending from L1
            board[startPos[0]][startPos[1]] = buildCode[player[levelIndex]]  # Update the board
            # Update the worker details and icon
            player[levelIndex] -= 1
            updateRef(pRef, player, refIndex, levelIndex)

        else:
            clearPos(startPos)

        workerLoc[workerLoc.index(startPos)] = newPos
        board[newPos[0]][newPos[1]] = player[refIndex]  # Update player position on the board

        return [newPos[0], newPos[1]]


def workerClimb(climbPos, playerLevel):
    """Correctly update worker level and detect if climbing, descending or jumping"""
    buildingLevel = findBuildLevel(climbPos)

    if (buildingLevel - 1) == playerLevel:  # Worker is going to climb up one level
        return True, buildingLevel

    elif buildingLevel == playerLevel:  # Worker going across buildings
        return True, str(buildingLevel)

    elif buildingLevel > playerLevel:  # Worker is descending
        return True, "desc"

    else:  # Standard movement detection
        return False, ""


def workerBuild(buildPos):
    """Allows selected worker to build on a specified space on the board"""
    if buildPos in workerLoc:  # Space is taken by a worker
        raise SelectionError
    elif buildPos not in buildLoc:  # Space not built on so know it's the first level
        newLevel = buildCode[1]
        buildLoc.append(buildPos)  # Store building position in taken locations to avoid collisions

    else:  # Building higher than l1
        if maxHeight(buildPos):
            raise SelectionError

        newLevel = buildCode[findBuildLevel(buildPos) + 1]

        # Remove old record from build details
        for i in range(len(buildDetails)):
            rec = buildDetails[i]
            if rec[0] == buildPos:
                buildDetails.remove(rec)
                break  # Prevent further searching

    board[buildPos[0]][buildPos[1]] = newLevel  # Update the board with new building position
    buildDetails.append([buildPos, newLevel])  # Add new record to building tracker


def newPosition(direction, pos):
    """Calculate new position by specified direction"""
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
    # Check use of returning pRef
    """Returns the player reference and the indexes for the specified workers reference and level"""
    pRef = stdRef(pRef)
    pRef = removeLevel(pRef)

    if pRef in ["A", "C"]:
        k, j = 0, 3
    else:
        k, j = 1, 4

    # Reference to the worker, worker tag and level index
    return pRef, j


def findBuildLevel(buildPos):
    """Find the level of a specified building and return it as an int"""
    for i in buildDetails:
        if i[0] == buildPos and i[1] != "| {} |":  # Find matching record
            return int(i[1].replace("|", "").replace(" ", "").replace("L", ""))  # Standardise reference


def updateRef(pRef, player, refIndex, levelIndex):
    """Take a player reference and update it"""
    player[refIndex] = "| {}{} |".format(removeLevel(stdRef(pRef)), player[levelIndex])  # Update worker reference
    if player[levelIndex] == 3:
        print("\nWow! Player {}, has won!".format(player[2]))
        exit()


def stdRef(ref):
    """Takes either a worker or building reference and only returns the letter or number"""
    return ref.replace("|", "").replace(" ", "").replace("L", "")


def removeLevel(ref):
    """Return given value without numerical values"""
    return ''.join([i for i in ref if not i.isdigit()])


def clearPos(startPos):
    """Clear a specified position from the board"""
    board[startPos[0]][startPos[1]] = "|    |"  # Clear icon from old position


def maxHeight(buildPos):
    if board[buildPos[0]][buildPos[1]] == "| {} |":
        return True


def outBounds(pos):
    if any(0 > val for val in pos) or any(val > 4 for val in pos):
        return True
