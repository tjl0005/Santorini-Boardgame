from exceptions import SelectionError, SpaceTakenError
from game import board, outBounds


def getStartPos(player, workerPos):
    """Uses user inputs to decide on the location for each of the workers and stores the input as coordinates"""
    while True:
        try:
            # PLayer selects their starting position, which is split
            pos1 = input("Select starting position (e.g. 2,2) for {}: ".format(player[0])).split(",")
            pos1 = [int(pos1[0]), int(pos1[1])]

            pos2 = input("Select starting position (e.g. 1,1) for {}: ".format(player[1])).split(",")
            pos2 = [int(pos2[0]), int(pos2[1])]

            check = checkStart(pos1, pos2, workerPos)

            return check

        except ValueError:
            print("One of more selections were invalid, try again.".format(player))
        except IndexError:
            print("Please match requested format, try again")
        except SpaceTakenError:
            print("A space you selected is taken, please try again")
        except SelectionError:
            print("Please enter a valid position")


def checkStart(pos1, pos2, workerPos):
    """Runs checks on the given start coordinates to ensure they are valid"""
    if pos1 == pos2:  # Current player already taken the space
        raise SpaceTakenError
    elif pos1 in workerPos or pos2 in workerPos:  # Other player taken the space
        raise SpaceTakenError
    elif outBounds(pos1) or outBounds(pos2):  # Given positions out of bounds
        raise SelectionError
    else:  # Valid position given
        validPos = pos1, pos2
        # Track all starting positions
        workerPos.append(validPos[0])
        workerPos.append(validPos[1])

        return validPos


def displayBoard():
    """Display the board properly in the console"""
    for i in board:
        print("------ ------ ------ ------ ------")
        print(" ".join(i))

    print("------ ------ ------ ------ ------")
