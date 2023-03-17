
from board import Board
from minimax import evaluate
from player import doRandomPlayerMove
from constants import Constants, PlayerTranspositionTable
import math
import pickle
#script that generates a dict in the format of 'boardsize , board : (bestMoveEval, bestMove)'

#(board) -> ()





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
    addToTable(board, moveWithGreatestEval, best_eval, player)
    if (depth == 0):
        board.doMove(moveWithGreatestEval, player)

    return best_eval


#----------------------------------------------generating the table

table_1 = {}
table_neg1 = {}
def addToTable(board, moveWithGreatestEval, best_eval, player):
    #stores the board, move and its eval in either table_1 (if player==1) or table_neg1 (if player ==-1)
    global table_1, table_neg1
    table = table_1 if player == 1 else table_neg1
    boardAsTouple = board.getTuple()
    if not boardAsTouple in table:
        table[boardAsTouple] = (moveWithGreatestEval, best_eval)

def gernerateTable(size):
    """
        Let two minimax algorithms play against each other on a board of size=size
    """
    b = Board(side_length=size, three_d=False)
    minimax(-1, 0, b)
    print(len(table_1))
    print(len(table_neg1))

    b = Board(side_length=size, three_d=False)
    minimax(1, 0, b)
    print(len(table_1))
    print(len(table_neg1))


    #write table into file
    filePath_1 = PlayerTranspositionTable.generateFilePath(Constants.TRANSPOSITION_TABLE_FILE_PATH, size, 1)
    with open(filePath_1, 'wb') as f:
        pickle.dump(table_1, f)

    filePath_neg1 = PlayerTranspositionTable.generateFilePath(Constants.TRANSPOSITION_TABLE_FILE_PATH, size, -1)
    with open(filePath_neg1, 'wb') as f:
        pickle.dump(table_neg1, f)

