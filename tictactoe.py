
import math, random, time
from player import Player
from board import Board
from constants import Constants, isAllowedToPrint


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




def playerMove(player, board):
    player.doMove(board)
    if isAllowedToPrint(message_verbosity=1, msgWhenSimulating=False):
        board.printBoard()
        print("")

def playGame(playerOne = Player(type=Player.RANDOM, playerIndex= 1), 
         playerTwo = Player(type=Player.MINIMAX_ALPHA_BETA, playerIndex = -1),
         boardsize = Constants.DEFAULT_BOARD_SIZE,
         threed = Constants.DEFAULT_THREE_D):
    
    if isAllowedToPrint(message_verbosity=0, msgWhenSimulating=False):
        print ("\n                   {0} vs {1}                \n".format(playerOne.getName(), playerTwo.getName()))

    board = Board(side_length = boardsize, three_d = threed)

    while(board.hasMoves() and board.hasWinner() == 0):

        playerMove(playerOne, board)
        if (not board.hasMoves() or not board.hasWinner() == 0):
            break

        playerMove(playerTwo, board)
    
    winner = board.hasWinner()

    if isAllowedToPrint(message_verbosity=0, msgWhenSimulating=False):
        if (winner == 0):
            print("draw!")
            
        elif (winner == 1):
            
            print("{0} has won!".format(playerOne.getName()))
        else:
            print("{0} has won!".format(playerTwo.getName()))

    return winner
#playGame(doMinimaxAlphaBetaPlayerMove, doMinimaxAlphaBetaPlayerMove, board)