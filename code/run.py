import sys
from ai import runMiniMax
from sillyAI import bot
from logger import Logger
from player import setBoard, playerChoice

playerA, playerB = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]
display = True

# Position players characters
posA, posB = setBoard(playerA)
posC, posD = setBoard(playerB)

decision = input("Please choose 2 Players (2) or EasyAI (Easy). ")


if decision == "2" or decision == "Two":
    while True:
        posA, posB = playerChoice([posA, posB], playerA)
        posC, posD = playerChoice([posC, posD], playerB)
elif decision == "easy" or decision == "Easy":
    sys.stdout = Logger()
    while True:
        # Store new coordinates to properly update on new turn
        posA, posB = playerChoice([posA, posB], playerA)
        posC = bot(posC, playerB, playerB[3], 0)
        posA, posB = playerChoice([posA, posB], playerA)
        posD = bot(posD, playerB, playerB[4], 1)
else:
    while True:
        posA, posB = playerChoice([posA, posB], playerA)
        posC = runMiniMax(posC, playerB)

