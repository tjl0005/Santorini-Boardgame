from game import newPosition, findBuildLevel, findWorkerLevel, getMoves


def getPossibleMoves(startPos, active, player, workerLoc, buildLoc):
    """Find all potential moves for a specified worker"""
    move, build, climb, descend = [], [], [], []

    for op in getMoves():
        pos = newPosition(op, startPos)

        if pos not in workerLoc and not any(0 < val > 4 for val in pos):  # Looking for valid spaces
            build.append(pos)  # Can build anywhere in bounds and without a worker

            if pos not in buildLoc:  # Empty space
                move.append(pos)

            else:  # Space has a building in it
                bLevel = findBuildLevel(pos)
                wLevel = findWorkerLevel(player[active])[2]

                if bLevel > player[wLevel]:  # Can climb it
                    climb.append(pos)
                else:  # Can only descend
                    descend.append(pos)

        return move, build, climb, descend


def minimax():
    return


def beam():
    return


def monte():
    return
