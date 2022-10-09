"""
This file is run to start the game and begin the selection for the play mode.
More details of the different play modes can be found within the README
"""

from AI.play_ai import easyAI, mediumAI
from Game.player import setBoard, playerOne, playerTwo, playerChoice
from Game.ui import moveCounter, userDecideStartPos

moveCount = 0  # Keep track of the number of moves taken
bot = False

userSelect = userDecideStartPos()  # If true the user will select the starting positions, otherwise default positions

# Place workers on the board and store their positions
posA, posB = setBoard(playerOne, userSelect)
posC, posD = setBoard(playerTwo, userSelect)

decision = input("Please choose 2 Players (2) or Vs. ")

try:
    while True:
        moveCount = moveCounter(moveCount)
        if decision in ["2", "Two", "two"]:
            posA, posB = playerChoice([posA, posB], playerOne)
            moveCount = moveCounter(moveCount)
            posC, posD = playerChoice([posC, posD], playerTwo)

        elif decision in ["vs", "Vs", "versus", "Versus"]:
            if not bot:
                bot = input("Greedy or Minimax? ")

            if bot in ["greedy", "Greedy"]:
                posA, posB = playerChoice([posA, posB], playerOne)
                moveCount = moveCounter(moveCount)
                posC, posD = easyAI([posC, posD], playerTwo)
            elif bot in ["min", "Min", "minimax", "Minimax"]:
                posA, posB = playerChoice([posA, posB], playerOne)
                moveCount = moveCounter(moveCount)
                posC, posD = mediumAI([posC, posD], playerTwo)
            else:
                raise ValueError

        elif decision == "bots":
            posA, posB = mediumAI([posA, posB], playerOne)
            moveCount = moveCounter(moveCount)
            posC, posD = easyAI([posC, posD], playerTwo)
        else:
            raise ValueError

except ValueError:
    print("Invalid selection, please try again")
