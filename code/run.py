from ai import playAI
from player import setBoard, playerChoice, initialPlayers

playerA, playerB = initialPlayers()

# Position players characters
posA, posB = setBoard(playerA)
posC, posD = setBoard(playerB)

decision = input("Please choose 2 Players (2) or Easy. ")

if decision == "2" or decision == "Two":
    while True:
        posA, posB = playerChoice([posA, posB], playerA)
        posC, posD = playerChoice([posC, posD], playerB)
else:
    while True:
        posA, posB = playerChoice([posA, posB], playerA)
        posC, posD = playAI([posC, posD], playerB)
