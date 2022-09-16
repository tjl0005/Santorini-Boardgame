from logger import startLog
from minimax import playMiniMax
from player import setBoard, playerChoice

playerOne, playerTwo = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]

startLog(False)  # Change to true if wanting to produce logs

# Position players workers and store said positions
posA, posB = setBoard(playerOne)
posC, posD = setBoard(playerTwo)

decision = input("Please choose 2 Players (2) or AI. ")

if decision in ["2", "Two", "two"]:
    while True:
        posA, posB = playerChoice([posA, posB], playerOne)
        posC, posD = playerChoice([posC, posD], playerTwo)
elif decision in ["vs", "versus", "Versus"]:
    while True:
        posA, posB = playMiniMax([posA, posB], playerOne)
        posC, posD = playMiniMax([posC, posD], playerTwo)
else:
    while True:
        posA, posB = playerChoice([posA, posB], playerOne)
        posC, posD = playMiniMax([posC, posD], playerTwo)
