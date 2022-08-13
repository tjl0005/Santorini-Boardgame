def prepPlayer(player, opponent):
    """Initialise character details"""
    startPos1, startPos2 = setStart(player, opponent)
    board[startPos1][startPos2] = player

    return startPos1, startPos2


def setStart(player, opponent):
    """Select character starting position"""
    while True:
        try:
            # PLayer selects their starting position
            startPos = input("Select starting position, e.g. 2,2, for {}: ".format(player))

            # Ensure space is free
            if startPos == opponent:
                raise KeyError

            startPos = startPos.split(",")

            return int(startPos[0]), int(startPos[1])

        except KeyError:
            print("Space taken, try again.")
        except ValueError:
            print("Invalid value, try again.".format(player))
        except IndexError:
            print("Requires a comma, try again")


def movePlayer(startPos, rivalPos, player):
    """Move relevant character across board"""
    while True:
        try:
            # Display board
            for i in board:
                print("----- ----- -----  ----- -----")
                print(" ".join(i))  # Show blank or occupied space

            print("----- ----- -----  ----- -----")

            # Get player move (WASD)
            move = input("{}'s Move: ".format(player))
            # Clear players current position from the board
            board[startPos[0]][startPos[1]] = "|   |"

            newPos = [startPos[0], startPos[1]]

            match move:
                case "W":
                    newPos[0] -= 1
                case "A":
                    newPos[1] -= 1
                case "S":
                    newPos[0] += 1
                case "D":
                    newPos[1] += 1

            if newPos == rivalPos:
                board[startPos[0]][startPos[1]] = player
                raise ValueError
            elif 5 in newPos or -1 in newPos:
                board[startPos[0]][startPos[1]] = player
                raise KeyError
            else:
                # Display character in new position
                board[newPos[0]][newPos[1]] = player

                return newPos[0], newPos[1]

        except ValueError:
            print("Space taken, please try again.")
        except KeyError:
            print("Out of bounds, please try again")


# Player icons
playerA, playerB = "| A |", "| B |"
# Generate board
board = [["|   |" for a in range(5)] for b in range(5)]

posX, posY = prepPlayer(playerA, None)
posZ, posA = prepPlayer(playerB, "{},{}".format(posX, posY))

while True:
    # Store new coordinates to properly update on new turn
    [posX, posY] = movePlayer([posX, posY], [posZ, posA], playerA)
    print(posX, posY)
    [posZ, posA] = movePlayer([posZ, posA], [posX, posY], playerB)