# Tic-tac-toe-everything

Tic-tac-toe-everything is a terminal-based tic-tac-toe application that enables you to play all kinds of tic-tac-toe games
First of all, not only regular $3 \times 3$ tic-tac-toe but any $n \times n$ tic-tac-toe. The next step is to play 3d-tic-tac-toe. <br>
This program provides basically three types of players; human, random and an AI - based on the minimax algorithm. Furthermore it allows you to simulate a number of games between players and gather data about those games. <br>
The real challenge is to write a fast enough algorithm for 3d tic-tac-toe.


## Usage and parameters

|Parameter | Explanation | Type | Default 
|:--:|:--|:--:|:--:|
|[playertype] | Type of players that play agains each other <br> first playertype is also player one | Integer <br> or String| 0
|-b, --board_size | Specifies the side-length of the board | Integer | 3
|-d, --three_d | If the game is 3D or not | bool | False
|-v, --verbosity | Specifies the amount of messages | Integer | 1
|-s, --simulate| Tells the program to simulate <br>a game between the two given players<br> the amount of specified times | Integer | -
|-t, --threads | Spcifies the amout of threads <br> when simulating | Integer | 1

### Playertypes

    RANDOM : 0 = 'random'
    HUMAN : 1 = 'human'
    MINIMAX : 2 = 'minimax'
    MINIMAX_ALPHA_BETA : 3 = 'minimax_ab'
    MINIMAX3D : 4 = 'minimax3d'

### Example 

```
  $ python3 tictactoe_interactive.py 1 1                         (1)
  $ python3 tictactoe_interactive.py 0 2  -s=1000 -t=2           (2)
  $ python3 tictactoe_interactive.py 4 4  -d=True -b=4           (3)
  $ python3 tictactoe_interactive.py human random  -d=True       (4)
```

- (1) is a regular tic-tac-toe game, where two human players play against each other
- (2) simulates 100 games on 2 threads (50 on each thread) where the first player is the random player and the second is the minimax algorithm
- (3) lets two minimax3D-Algrithms play against each other on a $4\times 4\times 4$ baord
- (4) is a 3d-game where the first player is human and the second player is random

### verbosity
The  verbosity and its effect differ, depending on if you are simulating games or not.

|Verbosity <br> Simulation| Effect|
|:-:|:-|
|0| Nothing is being printed besides simulation outcome
|1| Threads print out extrapolated time after a number of simulations
|2| Threads periodically print out status of simulation 

|Verbosity <br> Regular| Effect|
|:-:|:-|
|0| Print who is playing against who and the game-outcome|
|1| Print board after each move |
|2| minimax (regular and alpha beta pruning) prints out its move evaluation for depth 0 |
|3| minimax3d prints out evaluation for every baord |

## tic-tac-toe in 3d
The game is easily won by the first player if you play on a $3 \times 3 \times 3$, by just placing the first token in the center. 
Thats why tic-tac-toe in 3d if most regularly played on a $4 \times 4 \times 4$ board. <br>

## Minimax on an $n \times n \times n$ board
Anyway, the real challenge is to write a version of the minimax algroithm which is able to play tic-tac-toe in three dimensions.
### The brute force method
brute force soloutions would work by just giving the algorithm every empty cell in the tic-tac-toe cube as a possible square to move on. However the exploration tree would become so huge that this is really not a feasable solution (it would just take too long to find an answer).

### Currect idea
In the following i assume that $n$ is even.
My current idea, and the way the minimax3d algorithm currently works, is by slicing the cube into $2n$ 2d-boards ($n\times n$). These boards contain all possible diagonals, rows and columns that on which a player could win the game. <br>
The idea now is to evaluate every 2d-board with the minimax algorithm and find the best move over all boards. <br>
Problem : is that a board that is about to be lost has a realtively high (or low) score (for the opponent), compared to a board that is winnable. This way the  algorithm perfers making a move that would eventually win the game over making a move that would keep it from losing the game.




