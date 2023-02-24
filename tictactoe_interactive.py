import sys, getopt
import argparse
from player import Player
from board import Board
from tictactoe import playGame
from constants import Constants
from simulating import simulate

#interactive_arguments = sys.argv.pop(0)

#python3 tictactoe_interactive -v 1
"""
python3 tictactoe_interactive -v 1
python3 tictactoe_interactive -v=1
python3 tictactoe_interactive --verbosity 1
python3 tictactoe_interactive --verbosity=1
"""




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

def parseTypes(types):
    parsedTypes = []
    for type in types:
        if type.isdigit():
            parsedTypes.append(int(type))
        elif type == "random":
            parsedTypes.append(Player.RANDOM)
        elif type == "human":
            parsedTypes.append(Player.HUMAN)
        elif type == "minimax":
            parsedTypes.append(Player.MINIMAX)
        elif type == "minimax3d":
            parsedTypes.append(Player.MINIMAX3D)
        elif type == "minimax_ab":
            parsedTypes.append(Player.MINIMAX_ALPHA_BETA)
        else:
            parsedTypes.append(Player.RANDOM)
    return parsedTypes
        

def mainWithArgparse(argv):
    playertype_helpstring = "Type of player:\n random = 0\n human = 1\n minimax = 2\n minimax_alpha_beta = 3\n minimax3D = 4"
    parser = argparse.ArgumentParser(description="Get start and end dates")
    parser.add_argument('-b', '--board_size', help="board size", type=int, default=Constants.DEFAULT_BOARD_SIZE)
    parser.add_argument('-d', '--three_d', help="Boolean if board is 3d", type=bool, default=Constants.DEFAULT_THREE_D)

    parser.add_argument('-v', '--verbosity', help="System verbosity", default=Constants.DEFAULT_VERBOSITY)

    parser.add_argument('-s', '--simulate', help="Simulate the given number of games", type=int)
    parser.add_argument('-t', '--threads', help="Amount of simulation threads", type=int, default=Constants.DEFAULT_AMOUNT_THREADS)
    parser.add_argument('playertype', nargs=2, help=playertype_helpstring, default=[0,1])#nargs='*' for any number of args

    args = parser.parse_args()

    playertypes = parseTypes(args.playertype)
    Constants.SYSTEM_VERBOSITY = int(args.verbosity)
    pOne = Player(type=playertypes[0], playerIndex= 1)
    pTwo = Player(type=playertypes[1], playerIndex= -1)


    
    if not args.simulate:
        playGame(playerOne = pOne,
                playerTwo = pTwo,
                boardsize = args.board_size,
                threed = args.three_d)
        
    else:
        Constants.isSimulating = True
        #amountThreads, amountSimulations, playerOne, playerTwo, boardSize, threed
        simulate(amountThreads=args.threads,
                 amountSimulations=args.simulate,
                 playerOne=pOne,
                 playerTwo=pTwo,
                 boardSize=args.board_size,
                 threed=args.three_d)
    



mainWithArgparse(argv=sys.argv[1:])