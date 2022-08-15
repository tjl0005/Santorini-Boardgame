import re
from exceptions import SelectionError, BoundsError, SpaceTakenError
# TODO: Remove feature where you cannot build higher than current level, not a rule, oops
# TODO: Convert player lists into dictionaries in config
# TODO: Move counter
# TODO: Log

workerLoc = []
buildLoc = []
buildDetails = []

# Generate board
board = [["|    |" for a in range(5)] for b in range(5)]

buildCode = {
    0: "| L1 |",
    1: "| L2 |",
    2: "| L3 |",
    3: "| L4 |"
}


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

            worker = input("Select worker, {} or {} ? ".format(player[0], player[1]))

            # Player selected invalid character
            if worker not in ["A", "B", "C", "D"]:
                print("Fault 1")
                raise SelectionError

            active, static = workerIndex(worker)
            decision = input("Move or Build? ")

            if decision == "Move":
                startPos[active] = playerMove(player, startPos[active], worker)
                return startPos
            elif decision == "Build":
                playerBuild(startPos[active], player, active)
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


def playerMove(player, startPos, worker):
    move = input("Direction? ")

    active, static = workerIndex(worker)
    newPos = newPosition(move, [startPos[0], startPos[1]])

    if 5 in newPos or -1 in newPos:  # Player attempting to go out of bounds
        print("Fault 3")
        raise BoundsError
    elif newPos in workerLoc:  # Space in use by another player
        print("Fault 4")
        raise SpaceTakenError
    else:  # Standard movement
        if newPos in buildLoc:  # Check if space can be climbed and how so
            climb = playerClimb(newPos, player, active)

            if not climb[0]:  # Cannot climb
                print("Fault 5")
                raise BoundsError

            elif type(climb[1]) is int:  # Moving between buildings on same level
                board[startPos[0]][startPos[1]] = buildCode[climb[1] - 1]

            else:  # Going up a level
                if climb[1] > 0:  # If higher than L1 need to replace old building
                    board[startPos[0]][startPos[1]] = buildCode[climb[1] - 1]
                else:  # No building occupied so a blanks space
                    clearPos(startPos)

        elif startPos in buildLoc:  # Player descending
            currentLevel = findBuildLevel(startPos)
            board[startPos[0]][startPos[1]] = buildCode[currentLevel-1]

        else:
            clearPos(startPos)

        workerLoc[workerLoc.index(startPos)] = newPos
        board[newPos[0]][newPos[1]] = player[active]  # Update player position on the board

        return [newPos[0], newPos[1]]


def playerClimb(newPos, player, i):
    pRef, k, j = findWorkerLevel(player, i)
    buildingLevel = findBuildLevel(newPos)

    if (buildingLevel - 1) == player[j]:  # Player is going to climb up one level
        player[j] += 1  # Update player level
        pRef = re.sub("[0-9]", "", pRef)  # Remove level reference
        player[i] = "| {}{} |".format(pRef, player[j])  # Update player reference

        if player[j] == 3:
            print("Player {}, has won!".format(player[2]))
            exit()

        return True, True

    elif buildingLevel == player[j]:  # Worker going across buildings
        return True, buildingLevel

    else:  # Standard movement detection
        return False, ""


def playerBuild(startPos, player, i):
    move = input("Direction? ")

    buildPos = newPosition(move, [startPos[0], startPos[1]])

    if buildPos in workerLoc:  # Space is taken by a worker
        raise SelectionError
    elif buildPos not in buildLoc:  # Space not built on so know it's the first level
        newLevel = buildCode[0]
    else:  # Building higher than l1
        pRef, k, j = findWorkerLevel(player, i)
        buildLevel = findBuildLevel(buildPos)

        if buildLevel == player[j]:  # Check worker not attempting to build higher than valid level
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
    for i in buildDetails:
        if i[0] == buildPos:  # Find matching record
            return int(i[1].replace("|", "").replace(" ", "").replace("L", ""))  # Standardise reference


def workerIndex(worker):
    if worker == "A" or worker == "C":
        active, static = 0, 1
    elif worker == "B" or worker == "D":
        active, static = 1, 0
    else:
        raise SelectionError

    return active, static


def clearPos(startPos):
    board[startPos[0]][startPos[1]] = "|    |"  # Clear icon from old position


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
        case _:
            print("Fault 8")
            raise SelectionError()

    return newPos
