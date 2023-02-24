from minimax import minimaxAlphaBeta, minimax3d, minimax
import math, random

def doMinimaxPlayerMove(player, board):
    minimax(player, 0, board)

def doMinimaxAlphaBetaPlayerMove(player, board):
    minimaxAlphaBeta(player, 0, board, -math.inf, math.inf)

def doMinimax3dMove(player, board):
    minimax3d(player, board)
    

def doRandomPlayerMove(player, board):
    #ger random move and play it 
    moves = board.getPossibleMoves()
    move = moves[random.randint(0, len(moves) - 1)]
    board.doMove(move, player)

def doHumanPlayerMove(player, board):
    errorMessage = "Move string has to follow format : x,y. In case of 3d : plane,x,y"
    move_string = input("Input your move : ").strip()
    move = None
    try:
        move_coords = move_string.split(",")
        move = tuple(int(coord) for coord in move_coords) #creates a tuple (x, y, z)
    except:
        print(errorMessage)
        doHumanPlayerMove(player, board)
    
    try:
        if not board.isEmptyAt(move):
            print("Cannot move to given cell, because its not empty.")
            doHumanPlayerMove(player, board)

        board.doMove(player, move)
    except:
        print("Given index was probably out of bounds.")
        doHumanPlayerMove(player, board)

class Player:
    RANDOM = 0

    HUMAN = 1
    MINIMAX = 2
    MINIMAX_ALPHA_BETA = 3
    MINIMAX3D = 4

    AMOUNT_PLAYERS = 0

    def setup(type, index=""):
        name = ""
        playerFunction = None
        if type == Player.RANDOM:
            name = "Random_player"
            playerFunction = doRandomPlayerMove

        elif type == Player.MINIMAX or type == Player.MINIMAX_ALPHA_BETA or Player.MINIMAX3D:
            name = "Minimax_player"
            if type == Player.MINIMAX:
                playerFunction = doMinimaxPlayerMove
            elif type == Player.MINIMAX3D:
                playerFunction = doMinimax3dMove
                name += "(3D)"
            else:
                playerFunction = doMinimaxAlphaBetaPlayerMove
                name += "+alphaBeta"

        elif type == Player.HUMAN:
            name = "Human_player"
            playerFunction = doHumanPlayerMove
        return name + index, playerFunction


    def __init__(self, type=RANDOM, name_addon="", playerIndex=0):
        self.type = type

        #initialize variables
        self.name, self.playerFunction = Player.setup(type, name_addon)
        self.playerIndex = playerIndex
        self.player_number = Player.AMOUNT_PLAYERS
        Player.AMOUNT_PLAYERS += 1

    def doMove(self, board):
        self.playerFunction(self.playerIndex, board)

    def getName(self):
        return self.name
    
    def getUniqueName(self):
        return self.name + str(self.player_number)


player = Player(Player.MINIMAX, "#1")