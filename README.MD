# Tic-tac-toe

Idea :
1. Implement the minimax algorithm to play tic-tac-toe
2. Create a dataset, consisting of board configurations $c_i$ (9 input-parameters) and optimal moves $m_i$ with minimax 
3. Train a neural network with that dataset
4. Let the minimax algorithm play against the neural network


## Winner detection in 3d

Everyone knows how to detect a winner in 2d, just check if a player has $n$ crosses, or o's in line and if so, hes the winner. <br>
Even for arbitrary high $n$'s on an $n \times n$ board this algorithm does not change.<br>

However, in $3\text{D}$ thingd look a little differently. My idea was to rotate the entire $n \times n\times n$ cube, slice it into $n$ planes two times and check $n$ $n \times n$ boards two times:

```
Forward facing : 


    plane a                         plane b                     plane c
 a0  |  a1  |  a2             b0  |  b1  |  b2             c0  |  c1  |  c2
 a3  |  a4  |  a5             b3  |  b4  |  b5             c3  |  c4  |  c5
 a6  |  a7  |  a8             b6  |  b7  |  b8             c6  |  c7  |  c8 


 Rotated by 90° to the left: 
    plane a'                         plane b'                     plane c'
 a2  |  b2  |  c2             a1  |  b1  |  c1             a0  |  b0  |  c0
 a5  |  b5  |  c5             a4  |  b4  |  c4             a3  |  b3  |  c3
 a8  |  b8  |  c8             a7  |  b7  |  C7             a6  |  b6  |  c6 

Rotated by 90° to the right actually just switches plane a' and plane c'
```

### Computational advantage
The computational advantage of the rotaed board is simple : have a rotated copy of the tic-tac-toe cube and everytime the board
has to be searched for a winner, you can check $n$ planes of the forward facing cube and $n$ planes of the rotated cube ($+4 cube-diagonals$).
Because the rotation of each cell is only calculated once, there is no additional cost of placing a move inside the cube. <br>
