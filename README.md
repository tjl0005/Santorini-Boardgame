# Santorini-Bot
## Goals
The main goal of this project is to firstly, recreate a playable version of the board game Santorini in python. This implementation will contain all the features of the game but with a limitation on character choices and player amount, but these may be expanded upon.
Secondly is to implement artificial intelligence to compete against the player in a simulation of the game. A variety of algorithms including: heuristic search, e.g., minimax, beam search, Monte Carlo tree search.

## Santorini Walkthrough
#### Basics
•	2-4 players
•	Each player has 2 workers
  o	Able to move and climb
  o	Able to move and build (Base, Mid, Top and Dome)
  o	Both can move to adjacent squares
•	5 * 5 Checker-Board Layout
•	Turn Based -> Player can move worker and build once (unless otherwise specified)
•	First worker up to three levels wins
#### Characters
Provide unique buffs/skills:
•	Prometheus -> Worker can build if they do not move up (before and after moving)
•	Hephaestus -> Worker may build additional block (Not dome) on top of first block
•	Demeter -> Worker can build additional time but not on same space
•	Hermes -> If workers do not move up/down, they may move unlimited times (even zero)
#### Setup
•	No specific starting point
•	AI will decide because I don’t want to have to estimate best locations around player
•	Best to keep adjacent tiles free of workers for each player
#### Movement
•	Can move one space
•	Can build one level in an adjacent space (8 total) Progressing
•	Players can climb buildings
•	Incremental progression -> one layer at a time
•	First player up to third layer wins
•	Any player can build
•	Player can add 4th level, the dome, which means it cannot be climbed

## Simulating the Game
#### Board
2D Array, consisting of numbers and letters? Or would it need more dimensions?
#### Character
Limiting to four for reduced scope. Not intending to setup mechanics until events but just selection and descriptions.
Building
For each space there is an integer describing it -> store these integers in an array
Every time a player builds on a space the corresponding integer will increase by 1 -> starts at 0, ends at 4.
Cannot build after movement
#### Movement/Climbing
Player can move to adjacent eight spaces -> how to find those values?
Need a movement limit -> default 1 but can be changed by character buffs -> can only move before building unless specified.
Track current level -> default is 0 -> can only move to a space if it is less than current level plus 2 or new level 4-> ensures cannot climb more than one level or onto dome.
#### NOTE: the game should finish after level 3 is reached so might not be necessary or condition.
#### Events
Adjacent square occupied by player -> Need to track player positions and flag board values -> ignore when finding adjacent squares
Reaching level 3 -> trigger end -> display paths taken

#### NOTE: README is a continous work in progress and may not reflect current state
