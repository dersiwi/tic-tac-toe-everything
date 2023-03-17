from board import Board
import math
from constants import Constants 
from constants import printToUser, isAllowedToPrint


transposition_table_one = {}    #holds boards and best moves for player one
transposition_table_two = {}    #holds boards and best moves for player two
[transposition_table_one, transposition_table_two] #boardTuple : (bestMoveEval, bestMove)
transposition_hits = 0
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
    return winner * Constants.WIN_REWARD - winner * depth 


def minimax(player, depth, board):
    winner = board.hasWinner()
    if (depth >= Constants.MAX_DEPTH or not board.hasMoves() or winner != 0):
        return evaluate(depth, winner)
    
     #-inf if player is 1, inf if player is -1
    best_eval = (-1) * player * math.inf   
    moveWithGreatestEval = 0
    moves = board.getPossibleMoves()

    for move in moves:
        #do move and get evaluation of move, thinking the opponent plays optimally
        board.doMove(move, player)            
        moveEval = minimax((-1) * player, depth + 1, board)

        if (depth == 0):
            printToUser(str(move) + " : " + str(moveEval), message_verbosity=3, msgWhenSimulating=False)

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


def minimaxAlphaBeta(player, depth, board, alpha, beta, doMove=True):
        global transposition_hits
        winner = board.hasWinner()
        if (depth >= Constants.MAX_DEPTH or not board.hasMoves() or winner != 0):
            return evaluate(depth, winner)

        best_eval = alpha if player == 1 else beta   
        moveWithGreatestEval = 0
        moves = board.getPossibleMoves()


        for move in moves:
            #do move and get evaluation of move, thinking the opponent plays optimally
            
            board.doMove(move, player)
            if (player == -1):         
                moveEval = minimaxAlphaBeta((-1) * player, depth + 1, board, alpha, best_eval)
            else:
                moveEval = minimaxAlphaBeta((-1) * player, depth + 1, board, best_eval, beta)

            if (depth == 0):
                printToUser(str(move) + " : " + str(moveEval), message_verbosity=3, msgWhenSimulating=False)

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

        if (depth == 0 and doMove):
            board.doMove(moveWithGreatestEval, player)
        return best_eval


def minimax3d(player, board):
        global transposition_table_one, transposition_table_two

        best_eval = (-1) * player * math.inf   
        moveWithGreatestEval = 0
        slice_index = 0 #needed for converting 2d move into 3d move 
        boards = board.getAllSlices()

        transposition_table = transposition_table_one if player == 1 else transposition_table_two

        #get the best move over all two-d boards 
        for index ,twodBoard in enumerate(boards):
            twodBoard = Board(side_length=board.side_length, three_d=False, initBoard=twodBoard)

            #check if the board was already evaluated 
            boardTuple = twodBoard.getTuple()
            if boardTuple in transposition_table:
                bestBoardEval = transposition_table[boardTuple][0]
                bestBoardMove = transposition_table[boardTuple][1]
            else:
                #actually find the best move on this board, if board was not already evaluated
                twodMoves = twodBoard.getPossibleMoves()

                if isAllowedToPrint(message_verbosity=2, msgWhenSimulating=False):
                    print("")
                    twodBoard.printBoard()
                    
                bestBoardEval = (-1) * player * math.inf
                bestBoardMove = 0 
                for twodMove in twodMoves:
                    twodBoard.doMove(twodMove, player)
                    moveEval = minimaxAlphaBeta(player *(-1), 0, twodBoard, -math.inf, math.inf, doMove=False)
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

                #add board to transpo table
                transposition_table[boardTuple] = (bestBoardEval, bestBoardMove)
            printToUser(
                "best move on this board : {0}, eval : {1}. Current best eval : {2}\n".format(bestBoardMove, bestBoardEval, best_eval),
                message_verbosity=2,
                msgWhenSimulating=False
            )
                        
            if abs(bestBoardEval) > abs(best_eval):
                #force the algorithm to prevent a loss, rather than promote a win (if the lost is more immenent then the win)
                bestBoardEval *= (-1)

            if (player == -1):
                #minimize
                
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


        #if for some reason the algorithm has tow work on a 2d board
        if not board.three_d:
            board.doMove(moveWithGreatestEval, player)
            return
        
        #translate moveWithGreatestEval (2d move) into 3d move
        if slice_index < board.side_length:
            threedmove = (slice_index, moveWithGreatestEval[0], moveWithGreatestEval[1])
            board.doMove(threedmove, player)
            return
        elif slice_index < board.side_length * 2:
            threedmove = (slice_index - board.side_length, moveWithGreatestEval[0], moveWithGreatestEval[1])
            board.doMove(board.inversedRotationDict[threedmove], player)
            return
        elif slice_index == board.side_length*2:
            #first rotated board
            """
            actual 3d coordiantes of the board in question 3x3 example:
                (0,0,0)  |  (0,1,1)  |  (0,2,2) 
                (1,0,0)  |  (1,1,1)  |  (1,2,2)  
                (2,0,0)  |  (2,1,1)  |  (2,2,2)
            """
            threedmove = (moveWithGreatestEval[0], moveWithGreatestEval[1], moveWithGreatestEval[1])
            board.doMove(threedmove, player)
            return
        elif slice_index == board.side_length*2+1:
            #second rotated board
            """
            actual 3d coordiantes of the board in question 3x3 example:
                (0,2,0)  |  (0,1,1)  |  (0,0,2) 
                (1,2,0)  |  (1,1,1)  |  (1,0,2)  
                (2,2,0)  |  (2,1,0)  |  (2,0,2)
            (x,y) -> (i,j,k) = (x, side_length - y ,y)
            """
            threedmove = (moveWithGreatestEval[0], (board.side_length - 1) -moveWithGreatestEval[1], moveWithGreatestEval[1])
            board.doMove(threedmove, player)
            return


        
