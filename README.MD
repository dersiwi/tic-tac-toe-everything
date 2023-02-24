# Tic-tac-toe

Idea :
1. Implement the minimax algorithm to play tic-tac-toe
2. Create a dataset, consisting of board configurations $c_i$ (9 input-parameters) and optimal moves $m_i$ with minimax 
3. Train a neural network with that dataset
4. Let the minimax algorithm play against the neural network

The idea changed : My goal now is to write an algorithm that solves 3d-tic tac toe. 


### tic-tac-toe in 3d
The game is easily won by the first player if you play on a $3 \times 3 \times 3$, by just placing the first token in the center. <br>
Thats why tic-tac-toe in 3d if most regularly played on a $4 \times 4 \times 4$ board.


## Winner detection in 3d

My idea was to rotate the entire $n \times n\times n$ cube, slice it into $n$ planes two times and check $n$ $n \times n$ boards. 





## Board
The board class is a wrapper class for the game-board. The board is initiallized with the `side_length` of the board and if the board is $3\text{D}$ or not. Additionally you can give an `init_board` array to the baord-class, so the internal board will be initialized with that. This option however is only recommended for 2d-boards, as the rotated cube would not be up to date with the given board. (I did not implement this.)

### Functions
All functions work the same, independent of the board being $3\text{D}$ or $2\text{D}$.
- `hasWinner()` : which returns 0 if not and [-1, 1] if anyone of those has won 
- `hasMoves()` : False/True
- `getPossibleMoves()` : list of (move)-touples
- `doMove(move, player)` : places the player icon on the board
- `undoMove(move)` : marks the move as empty

In all cases is `move` a touple (depending on the dimension of the board eiter 2 or 3 entries) that specifies the indexes of the cell you want to place a move into. <br>

$3\text{D}$-only functions : 
- `getSlice(plane_index, rotated, angled)` : this functoin returns a $2\text{D}$-plane that is sliced out of the $3\text{D}$ cube. Each plane represents a $n \times n$ tic-tac-toe board.
  - `plane_index` : is between $[0, n-1]$ and specifies the planewhen looking directly at the cube
  - `rotated` : is a boolean, that specifies weathe the plane is sliced out of the regular cube (rotated == false) or out of the rotated cube 
  - `angled` :  is either [-1, 0, 1]. [1, -1] if the plane is rotated by 45°, or -45°. Can only be true, if $n$ is odd (so if there is a distinct center cell) and `plane_index` describes the plane in which that center cell lies. Put 0 if you do not want to
- `getAllSlices()` : returns an array of all possible slices of the cube. The first $n$ slices in the array are from the forward facing cube. The next $n$ slices are from the rotated cube.

These funcions do not fail in 2d, however, they just return the regular board on every call - no matter the parameters.