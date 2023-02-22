from tictactoe import doMinimaxPlayerMove, doRandomPlayerMove, doMinimaxAlphaBetaPlayerMove, doHumanPlayerMove

class Player:
    RANDOM = 0
    MINIMAX = 1
    MINIMAX_ALPHA_BETA = 2
    HUMAN = 3

    def getName(type, index=""):
        name = ""
        playerFunction = None
        if type == Player.RANDOM:
            name = "Random_player"
            playerFunction = doRandomPlayerMove

        elif type == Player.MINIMAX or type == Player.MINIMAX_ALPHA_BETA:
            name = "Minimax_player"
            if type == Player.MINIMAX:
                playerFunction = doMinimaxPlayerMove
            else:
                playerFunction = doMinimaxAlphaBetaPlayerMove

        elif type == Player.HUMAN:
            name = "Human_player"
            playerFunction = doHumanPlayerMove
        return name + index, playerFunction


    def __init__(self, type=RANDOM, name_addon="", playerIndex=0):
        self.type = type

        #initialize variables
        self.name, self.playerFunction = Player.getName(type, name_addon)
        self.playerIndex = playerIndex
        print(self.name)

    def doMove(self, board):
        self.playerFunction(self.playerIndex, board)


player = Player(Player.MINIMAX, "#1")