import sys, getopt
import argparse
from player import Player
from board import Board

#interactive_arguments = sys.argv.pop(0)

#python3 tictactoe_interactive -v 1
"""
python3 tictactoe_interactive -v 1
python3 tictactoe_interactive -v=1
python3 tictactoe_interactive --verbosity 1
python3 tictactoe_interactive --verbosity=1
"""


DEFAULT_VERBOSITY = 0
DEFAULT_BOARD_SIZE = 3
DEFAULT_THREE_D = False

SYSTEM_VERBOSITY = 0


def main(argv):
    global SYSTEM_VERBOSITY

    try:

        opts, args = getopt.getopt(argv, "v:", ["verbosity="])
        for opt, arg in opts:
            if opt in ['-v', '--verbosity']:
                SYSTEM_VERBOSITY = arg

        print(opts)
        print(SYSTEM_VERBOSITY)


    except getopt.GetoptError as err:
        print(err)


def mainWithArgparse(argv):
    global SYSTEM_VERBOSITY
    parser = argparse.ArgumentParser(description="Get start and end dates")
    parser.add_argument('-v', '--verbosity', help="System verbosity", default=DEFAULT_VERBOSITY)
    parser.add_argument('-b', '--board_size', help="board size", default=DEFAULT_BOARD_SIZE)
    parser.add_argument('-d', '--three_d', help="Boolean if board is 3d", type=int, default=DEFAULT_THREE_D)
    parser.add_argument('playertypes', nargs=2, type=int, help='Type of player')#nargs='*' for any number of args

    args = parser.parse_args()
    print(args.verbosity)
    playertypes = args.playertypes
    SYSTEM_VERBOSITY = int(args.verbosity)
    
    play(playerOne = Player(type=playertypes[0], playerIndex= 1),
            playerTwo = Player(type=playertypes[1], playerIndex= -1),
            boardsize = args.board_size,
            threed = args.three_d)
    

def playerMove(player, board):
    player.doMove(board)
    board.printBoard()
    print("")

def play(playerOne = Player(type=Player.RANDOM, playerIndex= 1), 
         playerTwo = Player(type=Player.MINIMAX_ALPHA_BETA, playerIndex = -1),
         boardsize = DEFAULT_BOARD_SIZE,
         threed = DEFAULT_THREE_D):
    
    print ("\n                   {0} vs {1}                \n".format(playerOne.getName(), playerTwo.getName()))

    board = Board(side_length = boardsize, three_d = threed)

    while(board.hasMoves() and board.hasWinner() == 0):

        playerMove(playerOne, board)
        if (not board.hasMoves() or not board.hasWinner() == 0):
            break

        playerMove(playerTwo, board)
    
    winner = board.hasWinner()
    if (winner == 0):
        print("draw!")
    elif (winner == 1):
        
        print("{0} has won!".format(playerOne.getName()))
    else:
        print("{0} has won!".format(playerTwo.getName()))

mainWithArgparse(argv=sys.argv[1:])