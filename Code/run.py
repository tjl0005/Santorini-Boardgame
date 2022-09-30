from Code.AI.greedy import easyAI
from Code.AI.minimax import mediumAI
from Code.Game.player import setBoard, playerOne, playerTwo, playerChoice

# Position players workers and store said positions
posA, posB = setBoard(playerOne)
posC, posD = setBoard(playerTwo)

decision = input("Please choose 2 Players (2) or Vs. ")
moveCount = 0

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
    while True:
        moveCount += 1
        posA, posB = mediumAI([posA, posB], playerOne)
        print("Move Count: {}".format(moveCount))
        posC, posD = easyAI([posC, posD], playerTwo)
        moveCount += 1
        print("Move Count: {}".format(moveCount))
