from ui import displayBoard
from logger import startLog
from minimax import playMiniMax
from player import setBoard, playerChoice, playerOne, playerTwo

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
        posA, posB = playerChoice([posA, posB], playerOne)
        displayBoard()
        posC, posD = playMiniMax([posC, posD], "Two")
else:
    while True:
        posA, posB = playMiniMax([posA, posB], "One")
        displayBoard()
        posC, posD = playMiniMax([posC, posD], "Two")
        displayBoard()
