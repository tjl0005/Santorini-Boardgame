# TODO: Attempt to build on another worker skips turn
# TODO: Worker label issue when climbing above level 1

def setStart(player):
    """Uses user inputs to decide on the location for each of the workers and stores the input as formatted coordinates
    in the format of [2,2] are converted into "2 2"
    Contains exceptions for formatting issues from the user
    """
    while True:
        try:
            # PLayer selects their starting position
            pos1 = input("Select starting position (e.g. 2,2) for {}: ".format(player[0]))
            pos2 = input("Select starting position (e.g. 1,1) for {}: ".format(player[1]))

            # Split input into individual coordinates
            pos1, pos2 = pos1.split(","), pos2.split(",")

            return checkStart(pos1, pos2)

        except ValueError:
            print("One of more selections were invalid, try again.".format(player))
        except IndexError:
            print("Please match requested format, try again")
        except SpaceTakenError:
            print("A space you selected is taken, please try again")
        except SelectionError:
            print("Please enter a valid position")


def checkStart(pos1, pos2):
    """Runs checks on the given start coordinates to ensure they are valid"""
    iPos1, iPos2 = [int(pos1[0]), int(pos1[1])], [int(pos2[0]), int(pos2[1])]

    if pos1 == pos2:  # Current player already taken the space
        raise SpaceTakenError
    elif iPos1 in workerLoc or iPos2 in workerLoc:  # Other player taken the space
        raise SpaceTakenError
    # elif any(0 < val > 4 for val in iPos1):  # Given positions out of bounds
    #     raise BoundsError
    else:  # Valid position given
        validPos = iPos1, iPos2
        # Track all starting positions
        workerLoc.append(validPos[0])
        workerLoc.append(validPos[1])

        return validPos


def prepPlayer(player):
    """Uses the setStart function twice to get the starting locations of each worker. The returned coordinates are then
    used to update the board with the locations of the workers and display them to the user."""
    startPos1, startPos2 = setStart(player)

    board[startPos1[0]][startPos1[1]] = player[0]
    board[startPos2[0]][startPos2[1]] = player[1]

    return startPos1, startPos2


def playerChoice(startPos, player):
    while True:
        try:
            # Display board
            for i in board:
                print("------ ------ ------ ------ ------")
                print(" ".join(i))

            print("------ ------ ------ ------ ------")

            print("Player {}".format(player[2]))

            worker = input("Select worker, {} or {} ? ".format(player[0], player[1]))

            # Player selected invalid character
            if worker not in ["A", "B", "C", "D"]:
                print("Fault 1")
                raise SelectionError
            # Select index for relevant characters coordinates
            elif worker == "A" or worker == "C":
                i, j = 0, 1
            else:
                i, j = 1, 0

            decision = input("Move or Build? ")

            if decision == "Move":
                return playerMove(player, startPos, i, j)
            elif decision == "Build":
                playerBuild(startPos[i], player, i)
                return startPos
            else:
                print("Fault 2")
                raise SelectionError

        except BoundsError:
            print("Out of bounds, please try again")
        except SpaceTakenError:
            print("Space taken, please try again")
        except SelectionError:
            print("Invalid selection, please try again.")


def playerMove(player, startPos, i, j):
    move = input("Direction? ")

    newPos = newPosition(move, [startPos[i][0], startPos[i][1]])

    # Player out of bounds
    if 5 in newPos or -1 in newPos:
        print(newPos)
        print("Fault 3")
        raise BoundsError
    elif newPos in workerLoc:  # Space in use by another player
        print("Fault 4")
        raise SpaceTakenError
    else:  # Standard movement
        # Check if space can be climbed
        if newPos in buildLoc:
            climb = playerClimb(newPos, player, i)
            if not climb[0]:
                print("Fault 5")
                raise BoundsError
            elif type(climb[1]) is int:
                board[startPos[i][0]][startPos[i][1]] = buildCode[climb[1]-1]  # Clear icon from old position
            else:
                board[startPos[i][0]][startPos[i][1]] = "|    |"  # Clear icon from old position
        else:
            board[startPos[i][0]][startPos[i][1]] = "|    |"  # Clear icon from old position

        if startPos[i] in workerLoc:
            workerLoc.remove(startPos[i])

        workerLoc.append(newPos)  # Track players new position
        board[newPos[0]][newPos[1]] = player[i]  # Update player position on the board

        return [newPos[0], newPos[1]], startPos[j]


def playerClimb(newPos, player, i):
    pRef, k, j = findWorkerLevel(player, i)

    buildingLevel = findBuildLevel(newPos)

    if (buildingLevel - 1) == player[j]:
        player[j] += 1
        player[i] = "| {}{} |".format(pRef, player[j]).replace("0", "")

        return True, True
    elif buildingLevel == player[j]:

        return True, buildingLevel
    else:
        return False, False


def playerBuild(startPos, player, i):
    move = input("Direction? ")

    buildPos = newPosition(move, [startPos[0], startPos[1]])

    if buildPos not in buildLoc and buildPos not in workerLoc:  # Space not built on or occupied by worker
        newLevel = buildCode[0]

    else:
        pRef, k, j = findWorkerLevel(player, i)
        buildLevel = findBuildLevel(buildPos)

        if buildLevel == player[j]:  # Prevents workers building on inaccessible spaces
            newLevel = buildCode[buildLevel]
        else:
            print("Fault 7")
            raise SelectionError

    board[buildPos[0]][buildPos[1]] = newLevel  # Update the board with new building position

    buildLoc.append(buildPos)  # Store building position in taken locations to avoid collisions
    buildDetails.append([buildPos, newLevel])  # Update building tracker


def findWorkerLevel(player, i):
    pRef = player[i].replace("|", "").replace(" ", "")  # Standardise reference

    if pRef == "A" or pRef == "C":
        k, j = 0, 3
    else:
        k, j = 1, 4

    # Reference to the worker, worker tag and level index
    return pRef, k, j


def findBuildLevel(buildPos):
    cLevel = ""
    for i in buildDetails:
        if i[0] == buildPos:  # Find matching record
            cLevel = i[1].replace("|", "").replace(" ", "").replace("L", "")  # Standardise reference

    return int(cLevel)


def newPosition(move, newPos):
    match move:
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
        case other:
            print("Fault 8")
            raise SelectionError()

    return newPos


class SpaceTakenError(Exception):
    """Player selecting an occupied space"""
    pass


class BoundsError(Exception):
    """Player attempting to go out of board limit"""
    pass


class SelectionError(Exception):
    """Player inputted invalid coordinates"""
    pass


class BuildLimitError(Exception):
    """Player hit build limit"""
    pass


playerA, playerB = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]
workerLoc = []
buildLoc = []
buildDetails = []

# Generate board
board = [["|    |" for a in range(5)] for b in range(5)]

# Position players characters
posA, posB = prepPlayer(playerA)
posC, posD = prepPlayer(playerB)

buildCode = {
    0: "| L1 |",
    1: "| L2 |",
    2: "| L3 |",
    3: "| L4 |"
}

while True:
    # Store new coordinates to properly update on new turn
    [posA, posB] = playerChoice([posA, posB], playerA)
    [posC, posD] = playerChoice([posC, posD], playerB)
