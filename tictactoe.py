
import math, random, time
player = 1
player_symbol_pos = 'x'
player_symbol_neg = 'o'
EMPTY = 0
MAX_DEPTH = math.inf
WIN_REWARD = 10
PRINT_MOVE_EVALUATION = False    #if true prints out evaluation of each move for depth==0

board = [0,0,0, 0,0,0, 0,0,0]



#testing boards
board1 = [-1,-1,-1 , 0,0,0, 0,0,0]
board2 = [0,-1,0,0,-1,-1 ,  0,-1,0]
board3 = [-1,0,0, 0,-1,0 , 0,0,-1]
board4 = [0,0,-1, 0,-1,0 , -1,0,0]


rows = columns = int(math.sqrt(len(board)))


def getSymbol(player):
    if (player == 1):
        return player_symbol_pos
    else:
        return player_symbol_neg

def printBoard(board):
    boardString = "\n"
    for i in range(rows):        
        for j in range(columns):
            if (board[i*rows + j] == 0):
                c = " "
            else:
                c = getSymbol(board[i*rows + j])
            boardString += "{:^3}".format(c)
            if (j < columns - 1):
                boardString += " | "
        boardString += "\n"
    print(boardString)



def getWinner(board):
    #return winner-index (-1) or (1) if a player has won, 0 if nobody has won yet
    diagonal1_sum = 0
    diagonal2_sum = 0
    for i in range(rows):
        rowsum = 0
        columnsum = 0
        
        for j in range(columns):
            #check if one player has all rows
            rowsum += board[i * rows + j]
            #check if one player has all columns
            columnsum += board[i + columns*j]
        if abs(rowsum) == rows:
            return int (rowsum / rows)
        if abs(columnsum) == columns:
            return int (columnsum / rows) 


        diagonal1_sum += board[i * (rows + 1)]  #0, 4, 8
        diagonal2_sum += board[(rows - 1) + i*(rows - 1)] #2, 4, 6
        if abs(diagonal1_sum) == rows:
            return int (diagonal1_sum / rows)
        if abs(diagonal2_sum) == columns:
            return int (diagonal2_sum / rows) 
    return 0



def hasMoves(board):    
    #true if positions of the board are empty
    for position in board:
        if position == EMPTY:
            return True
    return False

def evaluate(depth, winner):
    if (winner == 0):
        return 0
    #in case of winner ==1 returns 10 - depth, in case of -1 : -10+depth
    return winner * WIN_REWARD - winner * depth

def getPossibleMoves(board):
    #return indexes of all empty moves on the board
    moves = []
    for index, position in enumerate(board):
        if position == EMPTY:
            moves.append(index)
    return moves


def minimax(player, depth, board):
    winner = getWinner(board)
    if (depth >= MAX_DEPTH or not hasMoves(board) or winner != 0):
        return evaluate(depth, winner)
    
     #-inf if player is 1, inf if player is -1
    best_eval = (-1) * player * math.inf   
    moveWithGreatestEval = 0
    moves = getPossibleMoves(board)

    for move in moves:
        #do move and get evaluation of move, thinking the opponent plays optimally
        board[move] = player            
        moveEval = minimax((-1) * player, depth + 1, board)

        if (depth == 0) and PRINT_MOVE_EVALUATION:
            print(str(move) + " : " + str(moveEval))

        #undo move
        board[move] = EMPTY

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
        board[moveWithGreatestEval] = player

    return best_eval


def doMinimaxPlayerMove(player, board):
    minimax(player, 0, board)

def doRandomPlayerMove(player, board):
    #ger random move and play it 
    moves = getPossibleMoves(board)
    move = moves[random.randint(0, len(moves) - 1)]
    board[move] = player

def doHumanPlayerMove(player, board):
    move = int(input("Your move : "))
    if board[move] == EMPTY:
        board[move] = player
    else:
        doHumanPlayerMove(player)

def play():
    player = 1
    while(hasMoves(board) and getWinner(board) == 0):
        #minimax(player, 0)
        minimax(player, 0)
        printBoard(board)
        #player = player * (-1)
        doHumanPlayerMove((-1) * player)
        printBoard(board)

def playGame(playerOne, playerTwo, board, print=True):
    """
    params:
        playerOne, playerTwo have to be one of the functions : 
            - doRandomPlayerMove
            - doHumanPlayerMove
            - doMinimaxPlayerMove
        
        print=True means board is printed after every move, 
        print=False means nothing is printed

    return:
        getWinner(board) if a winner or draw has been determined
        if playerOne returns 1, if playerTwo won returns -1
    """
    player = 1
    while(hasMoves(board) and getWinner(board) == 0):
        playerOne(player, board)
        if print:
            printBoard(board)
        player = player * (-1)
        if (hasMoves(board) and getWinner(board) == 0):
            playerTwo(player, board)
            if print:
                printBoard(board)

        player = player * (-1)
    
    return getWinner(board)

