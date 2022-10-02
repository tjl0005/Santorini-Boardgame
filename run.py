"""
This file is run to start the game and begin the selection for the play mode.
More details of the different play modes can be found within the README
"""
from AI.greedy import easyAI
from AI.minimax import mediumAI
from Game.player import setBoard, playerOne, playerTwo, playerChoice

# Position players workers and store said positions
posA, posB = setBoard(playerOne)
posC, posD = setBoard(playerTwo)

decision = input("Please choose 2 Players (2) or Vs. ")

while True:
    try:
        if decision in ["2", "Two", "two"]:
            while True:
                posA, posB = playerChoice([posA, posB], playerOne)
                posC, posD = playerChoice([posC, posD], playerTwo)
        elif decision in ["vs", "Vs", "versus", "Versus"]:
            bot = input("Greedy or Minimax? ")
            if bot in ["greedy", "Greedy"]:
                while True:
                    posA, posB = playerChoice([posA, posB], playerOne)
                    posC, posD = easyAI([posC, posD], playerTwo)
            elif bot in ["min", "Min", "minimax", "Minimax"]:
                posA, posB = playerChoice([posA, posB], playerOne)
                posC, posD = mediumAI([posC, posD], playerTwo)
            else:
                raise ValueError
        else:
            moveCount = 0
            while True:
                moveCount += 1
                print("Move Count: {}".format(moveCount))
                posA, posB = mediumAI([posA, posB], playerOne)
                moveCount += 1
                print("Move Count: {}".format(moveCount))
                posC, posD = easyAI([posC, posD], playerTwo)

    except ValueError:
        print("Invalid selection, please try again.")
