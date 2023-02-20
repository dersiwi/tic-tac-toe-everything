

SIDE_LENGTH = 3
FIELDS = SIDE_LENGTH * SIDE_LENGTH

PLAYER_X = "x"
PLAYER_O = "o"
EMPTY = "-"



PLAYER_X_EVAL = 10
PLAYER_O_EVAL = -10

PLAYER_X_INDEX = 1
PLAYER_O_INDEX = -1

PLAYER_X_FUNCTION = None
PLAYER_O_FUNCITON = None

GAME_RUNNING = True
AI_MOVE = 0

board = [EMPTY] * FIELDS
bspBoard = [
PLAYER_X, EMPTY, EMPTY,
EMPTY, PLAYER_X, EMPTY, 
EMPTY,EMPTY, PLAYER_X]
bspBoard = [
PLAYER_O, EMPTY, PLAYER_X,
EMPTY, PLAYER_X, EMPTY, 
PLAYER_X,EMPTY, PLAYER_O]

def getEvalScore(playerIcon):
    if playerIcon == PLAYER_X:
        return PLAYER_X_EVAL
    if playerIcon == PLAYER_O:
        return PLAYER_O_EVAL

def getPlayerToken(playerIndex):
    if playerIndex == PLAYER_X_INDEX:
        return PLAYER_X
    if playerIndex == PLAYER_O_INDEX:
        return PLAYER_O

def evaluate(board):
    #rows 
    for i in range(SIDE_LENGTH):
        baseRowIndex = i * 3
        colEvaluation = evalThree(board, baseRowIndex, baseRowIndex + 1, baseRowIndex + 2)
        if colEvaluation != 0: return colEvaluation
    
    #cols 
    for i in range(SIDE_LENGTH):
        colEvaluation = evalThree(board, i, i + SIDE_LENGTH, i + 2*SIDE_LENGTH)
        if colEvaluation != 0: return colEvaluation


    #diagonals
    diag1Evaluation = evalThree(board, 0, 4, 8)
    if diag1Evaluation != 0: return diag1Evaluation
    diag2Evaluation = evalThree(board, 2, 4, 6)
    if diag2Evaluation != 0: return diag2Evaluation

    return 0
    
def evalThree(board, indexOne, indexTwo, indexThree):
    if (not board[indexOne] == EMPTY and board[indexOne] == board[indexTwo] and board[indexTwo] == board[indexThree]):  
        return getEvalScore(board[indexOne])
    return 0

def printBoard(board):
    boardString = ""
    for i in range(1, len(board) + 1):
        boardString += board[i - 1]
        if i == len(board):
            continue
        if i % 3 == 0:
            boardString += "\n"
        else:
            boardString += " |"

    print(boardString)



def makePlayerMove():
    move = input("Your move : ")
    moveAsInt = int(move)
    if moveAsInt < 1 or moveAsInt >= FIELDS +1 or board[moveAsInt - 1] != EMPTY:
        print("Illegal move. Only type 1-9. Also you can only move onto empty fields.")
        return makePlayerMove()
    return moveAsInt - 1

#--------------------------------------------------------------------------------MINIMAX ALGORITHM


def getPossibleMoves():
    pass

def makeMinimaxMove(playerToken, depth):
    possibleMoves = getPossibleMoves()
    bestMove = 0
    bestMoveEval = 0
    for move in possibleMoves:
        board[move] = playerToken
        evalMove = makeMinimaxMove(playerToken, depth + 1)
        
    pass



def minimax(playerIndex):
    possibleMoves = getPossibleMoves()
    maxValue = -1000

   

def maximize(player, depth):
    global AI_MOVE
    possibleMoves = getPossibleMoves()
    currBoardEval = evaluate()
    if possibleMoves == None or currBoardEval != 0:
        #board is either won or lost
        return currBoardEval

    maxValue = -1000

    for move in possibleMoves:
        board[move] = getPlayerToken(player)
        #eval all other moves
        moveValue = minimize(player * (-1), depth + 1)
        if moveValue > maxValue:
            maxValue = moveValue
            if depth == 0:
                AI_MOVE = move
        board[move] = EMPTY

def minimize(player, depth):
    pass


def makeMove(boardIndex, playerSymbol):
    board[boardIndex] = playerSymbol
    return evaluate(board)

def movePossible():
    for field in board:
        if not field == EMPTY:
            return True

    return False

def gameLoop():
    global GAME_RUNNING
    x_Function = PLAYER_X_FUNCTION
    o_Funciton = PLAYER_O_FUNCITON
    while GAME_RUNNING:
        printBoard(board)
        if (makeMove(x_Function(), PLAYER_X) == PLAYER_X_EVAL):
            print ("Player "+PLAYER_X+" won !")
            GAME_RUNNING = False
            continue
        printBoard(board)
        if not movePossible():
            print("Its a draw!")
        if (makeMove(o_Funciton(), PLAYER_O) == PLAYER_O_EVAL):
            print ("Player "+PLAYER_O+" won !")
            GAME_RUNNING = False
            continue
        if not movePossible():
            print("Its a draw!")
    printBoard(board)


def main():
    global PLAYER_X_FUNCTION, PLAYER_O_FUNCITON
    PLAYER_X_FUNCTION = makePlayerMove
    PLAYER_O_FUNCITON = makePlayerMove
    gameLoop()

main()