"""
This file is run to start the game and begin the selection for the play mode.
More details of the different play modes can be found within the README
"""

from AI.play_ai import easy_ai, medium_ai
from Game.player import set_board, playerOne, playerTwo, player_choice
from Game.ui import move_counter, user_decide_start_pos

moveCount = 0  # Keep track of the number of moves taken
bot = False

userSelect = user_decide_start_pos()  # If true the user will select the starting positions, otherwise default positions

# Place workers on the board and store their positions
posA, posB = set_board(playerOne, userSelect)
posC, posD = set_board(playerTwo, userSelect)

decision = input("Please choose 2 Players (2) or Vs. ")

try:
    while True:
        moveCount = move_counter(moveCount)
        if decision in ["2", "Two", "two"]:
            posA, posB = player_choice([posA, posB], playerOne)
            moveCount = move_counter(moveCount)
            posC, posD = player_choice([posC, posD], playerTwo)

        elif decision in ["vs", "Vs", "versus", "Versus"]:
            if not bot:
                bot = input("Greedy or Minimax? ")

            if bot in ["greedy", "Greedy"]:
                posA, posB = player_choice([posA, posB], playerOne)
                moveCount = move_counter(moveCount)
                posC, posD = easy_ai([posC, posD], playerTwo)
            elif bot in ["min", "Min", "minimax", "Minimax"]:
                posA, posB = player_choice([posA, posB], playerOne)
                moveCount = move_counter(moveCount)
                posC, posD = medium_ai([posC, posD], playerTwo)
            else:
                raise ValueError

        elif decision == "bots":
            posA, posB = medium_ai([posA, posB], playerOne)
            moveCount = move_counter(moveCount)
            posC, posD = easy_ai([posC, posD], playerTwo)
        else:
            raise ValueError

except ValueError:
    print("Invalid selection, please try again")
