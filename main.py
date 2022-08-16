import sys
from game import playerChoice, prepPlayer
from logger import Logger

playerA, playerB = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]

# Position players characters
posA, posB = prepPlayer(playerA)
posC, posD = prepPlayer(playerB)

sys.stdout = Logger()    # Log does not currently save input so starting after initial inputs

while True:
    # Store new coordinates to properly update on new turn
    posA, posB = playerChoice([posA, posB], playerA)
    posC, posD = playerChoice([posC, posD], playerB)
