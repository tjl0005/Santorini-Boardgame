from ui import displayBoard
from logger import startLog
from minimax import decideMove
from player import setBoard, playerChoice, playerOne, playerTwo


startLog(False)  # Change to true if wanting to produce logs

# Position players workers and store said positions
posA, posB = setBoard(playerOne)
posC, posD = setBoard(playerTwo)

decision = input("Please choose 2 Players (2) or AI. ")
moveCount = 0

if decision in ["2", "Two", "two"]:
    while True:
        posA, posB = playerChoice([posA, posB], playerOne)
        posC, posD = playerChoice([posC, posD], playerTwo)
elif decision in ["vs", "versus", "Versus"]:
    while True:
        posA, posB = playerChoice([posA, posB], playerOne)
        displayBoard()
        posC, posD = decideMove([posC, posD], playerTwo)
else:
    while True:
        moveCount += 1
        posA, posB = decideMove([posA, posB], playerOne)
        print("Move Count: {}".format(moveCount))
        displayBoard()
        posC, posD = decideMove([posC, posD], playerTwo)
        moveCount += 1
        print("Move Count: {}".format(moveCount))
        displayBoard()
