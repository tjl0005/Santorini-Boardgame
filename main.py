from game import playerChoice, prepPlayer

playerA, playerB = ["| A0 |", "| B0 |", "One", 0, 0], ["| C0 |", "| D0 |", "Two", 0, 0]

# Position players characters
posA, posB = prepPlayer(playerA)
posC, posD = prepPlayer(playerB)

while True:
    # Store new coordinates to properly update on new turn
    posA, posB = playerChoice([posA, posB], playerA)
    posC, posD = playerChoice([posC, posD], playerB)
