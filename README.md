# Santorini-Bot

### Breakdown and Future Aspirations

This project implements a fully playable version of the board game Santorini in Python, with different play modes.
Currently, a two player mode as well as a versus mode.

The versus mode is hoped to be expanded upon using Monte Carlo Search and potentially further refining of the current
MiniMax implementation.

### Playing the Game

When running the code you will be firstly asked for the starting points of the workers.
These inputs are validated and must be in the form of "2,1". Where the first number represents the row and the second
represents the column. Then you will be asked to select your play mode, either two players (You and yourself or someone
else) or bot. If you choose to face a bot you can either play against the easy implementation
(Using a greedy approach) or the difficult (Currently medium and uses minimax) to play against.
Once this selection is made you will be prompted to select a worker and decide if you want to move or build.

You select the tile you want using the WASD keys, and you can move diagonally by combining directions e.g. Left/Up is WA
.

The game will end when a player has a worker on level 3. More details on playing the game are below.

### Santorini Walk-through

A great guide is available at: https://en.boardgamearena.com/doc/Tips_santorini and a basic rundown of the game is below

#### Basics

* Currently, just 2 players
* Each player has 2 workers
    * Able to move and climb
    * Able to move and build (Base, Mid, Top and Dome)
    * Able move to adjacent squares
* 5 * 5 Checker-Board Layout
* Turn Based, a player can either move worker or build once (unless otherwise specified)
* First worker up to three levels wins

#### Characters

Provide unique buffs/skills:

* Prometheus: Worker can build if they do not move up (before and after moving)
* Hephaestus: Worker may build additional block (Not dome) on top of first block
* Demeter: Worker can build additional time but not on same space
* Hermes: If workers do not move up/down, they may move unlimited times (even zero)

#### Setup

* Workers can be placed on any empty space on the board
* Best to keep adjacent tiles free of workers for each player

#### Movement

* Can move one space
* Can build one level in an adjacent space (8 total) Progressing
* Players can climb and descend buildings
* Incremental progression you can climb one level at a time
* First player up to third level wins
* Any player can build
* Player can add 4th level, the dome, which means it cannot be climbed anymore.