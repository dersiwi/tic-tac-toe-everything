
import math
player = 1
EMPTY = 0
MAX_DEPTH = math.inf
WIN_REWARD = 100

board = [0,0,0, 0,0,0, 0,0,0]



#testing boards
board1 = [-1,-1,-1 , 0,0,0, 0,0,0]
board2 = [0,-1,0,0,-1,-1 ,  0,-1,0]
board3 = [-1,0,0, 0,-1,0 , 0,0,-1]
board4 = [0,0,-1, 0,-1,0 , -1,0,0]


rows = columns = int(math.sqrt(len(board)))


def printBoard(board):
    boardString = ""
    for i in range(rows):        
        for j in range(columns):
            if (board[i*rows + j] == 0):
                boardString += " "
            else:
                boardString += str(board[i*rows + j])
            if (j < columns - 1):
                boardString += " | "
        boardString += "\n"
    print(boardString)



def getWinner(board):
    #return winner_index (-1) or (1) if a player has won
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

def maximize(player, depth):
    winner = getWinner(board)
    if (depth >= MAX_DEPTH or not hasMoves(board) or winner != 0):
        return evaluate(depth, winner)

    maxEval = -math.inf
    moveWithMaxEval = 0
    moves = getPossibleMoves(board)
    for move in moves:
        board[move] = player
        moveEval = minimize( (-1) * player, depth + 1)
        board[move] = EMPTY
        if (moveEval > maxEval):
            maxEval = moveEval
            moveWithMaxEval = move

    if (depth == 0):
        board[moveWithMaxEval] = player
    return maxEval



def minimize(player, depth):
    winner = getWinner(board)
    if (depth >= MAX_DEPTH or not hasMoves(board) or winner != 0):
        return evaluate(depth, winner)
    
    minEval = math.inf
    moveWithMinEval = 0
    moves = getPossibleMoves(board)

    for move in moves:
        board[move] = player
        moveEval = maximize( (-1) * player, depth + 1)
        board[move] = EMPTY
        if (moveEval < minEval):
            minEval = moveEval
            moveWithMinEval = move

    if (depth == 0):
        board[moveWithMinEval] = player
    return minEval
    
def doMove(player):
    if (player == -1):
        minimize(player, 0)
    else:
        maximize(player, 0)
    

def play():
    player =1
    while(hasMoves(board)):
        doMove(player)
        printBoard(board)
        player = player * (-1)

play()