def setStart(player):
    """Select character starting position"""
    while True:
        try:
            # PLayer selects their starting position
            pos1 = input("Select starting position, e.g. 2,2, for {}: ".format(player[0]))
            pos2 = input("Select starting position, e.g. 2,2, for {}: ".format(player[1]))

            pos1 = pos1.split(",")
            pos2 = pos2.split(",")

            return [int(pos1[0]), int(pos1[1])], [int(pos2[0]), int(pos2[1])]

        except ValueError:
            print("Invalid value, try again.".format(player))
        except IndexError:
            print("Requires a comma, try again")


def prepPlayer(player):
    """Initialise character details"""
    startPos1, startPos2 = setStart(player)

    board[startPos1[0]][startPos1[1]] = player[0]
    board[startPos2[0]][startPos2[1]] = player[1]

    return startPos1, startPos2


def movePlayer(startPos, player):
    """Move relevant character across board"""
    while True:
        # print("{}: {} and {}: {}".format(player[0], startPos[0], player[1], startPos[1]))
        try:
            # Display board
            for i in board:
                print("----- ----- ----- ----- -----")
                print(" ".join(i))  # Show blank or occupied space

            print("----- ----- ----- ----- -----")

            print("{} / {}'s Move".format(player[0], player[1]))
            character = input("Select worker, {} or {} ? ".format(player[0], player[1]))

            if character == "A" or character == "C":
                i = 0
            elif character not in characters:
                raise AssertionError
            else:
                i = 1

            # print("{}: {}, {}".format(character, startPos[i][0], startPos[i][1]))

            # Clear players current position from the board
            board[startPos[i][0]][startPos[i][1]] = "|   |"

            # Get player move (WASD)
            move = input("Direction? ")
            newPos = [startPos[i][0], startPos[i][1]]

            match move:
                case "W":
                    newPos[0] -= 1
                case "A":
                    newPos[1] -= 1
                case "S":
                    newPos[0] += 1
                case "D":
                    newPos[1] += 1

            # print("{}: {}".format(character, newPos))

            if 5 in newPos or -1 in newPos:
                board[startPos[0]][startPos[1]] = player[i]
                raise KeyError
            else:
                # Display character in new position
                board[newPos[0]][newPos[1]] = player[i]

                if i == 0:
                    nI = 1
                else:
                    nI = 0

                return [newPos[0], newPos[1]], startPos[nI]

        except KeyError:
            print("Out of bounds, please try again")
        except AssertionError:
            print("Invalid worker selection, please try again.")


# Player icons
playerA, playerB = ["| A |", "| B |"], ["| C |", "| D |"]
characters = ["A", "B", "C", "D"]
# Generate board
board = [["|   |" for a in range(5)] for b in range(5)]

posA, posB = prepPlayer(playerA)
posC, posD = prepPlayer(playerB)

# posA = board[2][1] = playerA[0]
# posB = board[2][2] = playerA[1]
# posC = board[2][3] = playerB[0]
# posD = board[2][4] = playerB[1]

while True:
    print("A: {}, B: {}".format(posA, posB))
    # Store new coordinates to properly update on new turn
    [posA, posB] = movePlayer([posA, posB], playerA)
    print("A: {}, B: {}".format(posA, posB))
    [posC, posD] = movePlayer([posC, posD], playerB)
    print("C: {}, D: {}".format(posC, posD))