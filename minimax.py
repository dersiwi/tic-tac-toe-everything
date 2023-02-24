from board import Board
import math

MAX_DEPTH = 10
WIN_REWARD = MAX_DEPTH + 1
PRINT_MOVE_EVALUATION = True
PRINT_DEPTH = 0

transposition_table = {} #position : vallue by minimax
"""
position : vallue by minimax

 1  |  0  |  0
 0  |  0  |  0
 0  |  0  |  0 

 1  | -1  |  0            1  |  0  |  0
 0  |  0  |  0           -1  |  0  |  0
 0  |  0  |  0            0  |  0  |  0 

 1  | -1  |  0            1  |  0  |  0
 0  |  1  |  0           -1  |  1  |  0
 0  |  0  |  0            0  |  0  |  0   

 1  | -1  |  0            1  | -1  |  0     <-- same position, although different move orders
-1  |  1  |  0           -1  |  1  |  0
 0  |  0  |  0            0  |  0  |  0        

"""

#evaluate function for all minimax algorithms
def evaluate(depth, winner):
    if (winner == 0):
        return 0
    #in case of winner ==1 returns 10 - depth, in case of -1 : -10+depth
    return winner * WIN_REWARD - winner * depth 


def minimax(player, depth, board):
    winner = board.hasWinner()
    if (depth >= MAX_DEPTH or not board.hasMoves() or winner != 0):
        return evaluate(depth, winner)
    
     #-inf if player is 1, inf if player is -1
    best_eval = (-1) * player * math.inf   
    moveWithGreatestEval = 0
    moves = board.getPossibleMoves()

    for move in moves:
        #do move and get evaluation of move, thinking the opponent plays optimally
        board.doMove(move, player)            
        moveEval = minimax((-1) * player, depth + 1, board)

        if (depth == 0) and PRINT_MOVE_EVALUATION:
            print(str(move) + " : " + str(moveEval))

        #undo move
        board.undoMove(move)

        #if move was better then the previous best move, update
        if (player == -1):
            #minimize
            if (moveEval < best_eval):
                best_eval = moveEval
                moveWithGreatestEval = move
        else:
            #maximize
            if (moveEval > best_eval):
                best_eval = moveEval
                moveWithGreatestEval = move

    if (depth == 0):
        board.doMove(moveWithGreatestEval, player)

    return best_eval


def minimaxAlphaBeta(player, depth, board, alpha, beta):
        winner = board.hasWinner()
        if (depth >= MAX_DEPTH or not board.hasMoves() or winner != 0):
            return evaluate(depth, winner)

        best_eval = (-1) * player * math.inf   
        moveWithGreatestEval = 0
        moves = board.getPossibleMoves()

        for move in moves:
            #do move and get evaluation of move, thinking the opponent plays optimally
            board.doMove(move, player)
            if (player == -1):         
                moveEval = minimaxAlphaBeta((-1) * player, depth + 1, board, alpha, best_eval)
            else:
                moveEval = minimaxAlphaBeta((-1) * player, depth + 1, board, best_eval, beta)

            if (depth == PRINT_DEPTH) and PRINT_MOVE_EVALUATION:
                print(str(move) + " : " + str(moveEval))
                
            board.undoMove(move)

            #if move was better then the previous best move, update
            if (player == -1):
                #minimize
                if (moveEval < best_eval):
                    best_eval = moveEval
                    moveWithGreatestEval = move
                if (best_eval <= alpha):
                    break
            else:
                #maximize
                if (moveEval > best_eval):
                    best_eval = moveEval
                    moveWithGreatestEval = move
                if (best_eval >= beta):
                    break

        if (depth == 0):
            board.doMove(moveWithGreatestEval, player)
        return best_eval


def minimax3d(player, board):
        best_eval = (-1) * player * math.inf   
        moveWithGreatestEval = 0
        slice_index = 0 #needed for converting 2d move into 3d move 
        boards = board.getAllSlices()

        #get the best move over all two-d boards 
        for index ,twodBoard in enumerate(boards):
            twodBoard = Board(side_length=board.side_length, three_d=False, initBoard=twodBoard)
            twodMoves = twodBoard.getPossibleMoves()
            print("")
            twodBoard.printBoard()
            bestBoardEval = (-1) * player * math.inf
            bestBoardMove = 0 
            for twodMove in twodMoves:
                twodBoard.doMove(twodMove, player)
                moveEval = minimaxAlphaBeta(player *(-1), 1, twodBoard, -math.inf, math.inf)
                twodBoard.undoMove(twodMove)

                if (player == -1):
                    #minimize
                    if (moveEval < bestBoardEval):
                        bestBoardEval = moveEval
                        bestBoardMove = twodMove
                else:
                    #maximize
                    if (moveEval > bestBoardEval):
                        bestBoardEval = moveEval
                        bestBoardMove = twodMove
            print("best move on this board : {0}, eval : {1}. Current best eval : {2}\n".format(bestBoardMove, bestBoardEval, best_eval))
                        
            
            if (player == -1):
                #minimize
                bestBoardEval *= (-1)
                if (bestBoardEval < best_eval):
                    best_eval = bestBoardEval
                    moveWithGreatestEval = bestBoardMove
                    slice_index = index
            else:
                #maximize
                if (bestBoardEval > best_eval):
                    best_eval = bestBoardEval
                    moveWithGreatestEval = bestBoardMove
                    slice_index = index

        #translate 2d move into 3d move
        
        if slice_index < board.side_length:
            threedmove = (slice_index, moveWithGreatestEval[0], moveWithGreatestEval[1])
            board.doMove(threedmove, player)
        else:
            threedmove = (slice_index - board.side_length, moveWithGreatestEval[0], moveWithGreatestEval[1])
            board.doMove(board.inversedRotationDict[threedmove], player)

        
                



"""def play():
    player = 1
    board = Board(side_length=3, three_d=True)
    while(board.hasMoves() and board.hasWinner() == 0):
        #minimax(player, 0)
        minimax3d(player, board)
        board.printBoard()
        print("")
        player = (-1)*player
        continue

play()"""

def doHumanPlayerMove(player, board):
    print(board.getPossibleMoves())
    move_x = int(input("Your move x : "))
    move_y = int(input("Your move y : "))

    board.doMove((move_x, move_y), player)

def play():
    player = 1
    board = Board(side_length=3, three_d=False)
    while(board.hasMoves() and board.hasWinner() == 0):
        #minimax(player, 0)
        if player == 1:
            minimaxAlphaBeta(player, 0, board, -math.inf, math.inf)
            
        else:
            doHumanPlayerMove(player, board)
        board.printBoard()
        print("")
        player = (-1)*player
        continue

#play()