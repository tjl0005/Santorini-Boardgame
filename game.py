import re
from exceptions import SelectionError, BoundsError, SpaceTakenError

workerLoc = []
buildLoc = []
buildDetails = []
moves = ["W", "A", "S", "D", "WA", "WD", "SA", "SD"]

# Generate board
board = [["|    |" for a in range(5)] for b in range(5)]

buildCode = {
    1: "| L1 |",
    2: "| L2 |",
    3: "| L3 |",
    4: "| () |"
}


def getBuildDetails():
    return buildDetails


def getWorkerLoc():
    return workerLoc


def getBuildLoc():
    return buildLoc


def workerMove(player, startPos, active, newPos):
    """Complete task of moving the player on the board and detecting if selected movement requires a worker to climb
    or descend"""

    if 5 in newPos or -1 in newPos:  # Player attempting to go out of bounds
        print("Fault 3")
        raise BoundsError
    elif newPos in workerLoc:  # Space in use by another player
        print("Fault 4")
        raise SpaceTakenError
    else:  # Standard movement
        if newPos in buildLoc:  # Check if space can be climbed and how so
            climb = workerClimb(newPos, player, active)

            if not climb[0]:  # Cannot climb
                print("Fault 5")
                raise BoundsError

            elif type(climb[1]) is str:  # Moving between buildings on same level
                if climb[1] == "desc":
                    print("Detected as going down again")
                    currentLevel = findBuildLevel(startPos)
                    board[startPos[0]][startPos[1]] = buildCode[currentLevel]
                    board[startPos[0]][startPos[1]] = buildCode[currentLevel]
                else:
                    print("Moving between same level buildings")
                    print(climb[1])
                    board[startPos[0]][startPos[1]] = buildCode[int(climb[1])]

            else:  # Going up a level
                if climb[1] > 1:  # If higher than L1 need to replace old building
                    print("Climbing higher than L1")
                    board[startPos[0]][startPos[1]] = buildCode[climb[1] - 1]
                else:  # No building occupied so a blanks space
                    print("Climbing L1, so clearing old position")
                    clearPos(startPos)

        elif startPos in buildLoc:  # Player descending from L1
            currentLevel = findBuildLevel(startPos)
            board[startPos[0]][startPos[1]] = buildCode[currentLevel]
            print("Player descending")

        else:
            print("Standard movement")
            clearPos(startPos)

        workerLoc[workerLoc.index(startPos)] = newPos
        board[newPos[0]][newPos[1]] = player[active]  # Update player position on the board

        return [newPos[0], newPos[1]]


def workerClimb(newPos, player, i):
    """Correctly update worker level and detect if climbing, descending or jumping"""
    pRef, k, j = findWorkerLevel(player, i)
    buildingLevel = findBuildLevel(newPos)

    if (buildingLevel - 1) == player[j]:  # Worker is going to climb up one level
        print("Worker climbing up a level")
        player[j] += 1  # Update worker level
        updateRef(pRef, player, i, j)

        return True, buildingLevel

    elif buildingLevel == player[j]:  # Worker going across buildings
        print("Going across buildings")
        return True, str(buildingLevel)

    elif player[j] > buildingLevel:
        print("Player descending building higher than L1")
        player[j] -= 1
        updateRef(pRef, player, i, j)

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
        buildLevel = findBuildLevel(buildPos)

        newLevel = buildCode[buildLevel + 1]

        # Remove old record from build details
        for i in range(len(buildDetails)):
            rec = buildDetails[i]
            if rec[0] == buildPos:
                buildDetails.remove(rec)
                break

    board[buildPos[0]][buildPos[1]] = newLevel  # Update the board with new building position

    buildDetails.append([buildPos, newLevel])  # Add new record to building tracker


def findWorkerLevel(player, i):
    # Check use of returning pRef
    """Returns the player reference and the indexes for the specified workers reference and level"""
    pRef = player[i].replace("|", "").replace(" ", "")  # Standardise reference
    pRef = re.sub("[0-9]", "", pRef)
    if pRef == "A" or pRef == "C":
        k, j = 0, 3
    else:
        k, j = 1, 4

    # Reference to the worker, worker tag and level index
    return pRef, k, j


def findBuildLevel(buildPos):
    """Find the level of a specified building and return it as an int"""
    for i in buildDetails:
        print(i[0])
        if i[0] == buildPos and i[1] != "| () |":  # Find matching record
            return int(i[1].replace("|", "").replace(" ", "").replace("L", ""))  # Standardise reference


def clearPos(startPos):
    """Clear a specified position from the board"""
    board[startPos[0]][startPos[1]] = "|    |"  # Clear icon from old position


def updateRef(pRef, player, i, j):
    """Take a player reference and update it"""
    # Test if old pRef required
    pRef = re.sub("[0-9]", "", pRef)  # Remove level reference
    player[i] = "| {}{} |".format(pRef, player[j])  # Update worker reference

    if player[j] == 3:
        print("Player {}, has won!".format(player[2]))
        exit()


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
