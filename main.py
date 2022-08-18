import sys

from ai import basicAI
from logger import Logger
from player import prepPlayer, playerChoice

playerA, playerB = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]
display = True

# Position players characters
posA, posB = prepPlayer(playerA)
posC, posD = prepPlayer(playerB)

# sys.stdout = Logger()    # Log does not save input so starting after initial inputs

while True:
    # Store new coordinates to properly update on new turn
    posA, posB = playerChoice([posA, posB], playerA)
    # posC, posD = playerChoice([posC, posD], playerB)
    posC, posD = basicAI([posC, posD], playerB)
    # posC, posD = basicAI(posC, playerB, bDetails())
