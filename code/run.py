from ai import playAI
from player import setBoard, playerChoice, initialSetup

playerA, playerB = initialSetup()

# Position players characters
posA, posB = setBoard(playerA)
posC, posD = setBoard(playerB)

decision = input("Please choose 2 Players (2) or Easy. ")


if decision in [2, "Two", "two"]:
    while True:
        posA, posB = playerChoice([posA, posB], playerA)
        posC, posD = playerChoice([posC, posD], playerB)
else:
    while True:
        posA, posB = playerChoice([posA, posB], playerA)
        posC, posD = playAI([posC, posD], playerB)
