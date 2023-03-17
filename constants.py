import pickle

class TranspositionTable:
    def __init__(self):
        self.tp_table_1 = None
        self.tp_tbale_neg1 = None

    def load(self, board_size):
        self.tp_table_1 = PlayerTranspositionTable(boardSize=board_size, player=1)
        self.tp_tbale_neg1 = PlayerTranspositionTable(boardSize=board_size, player=-1)

    def getMoveEvalPair(self, boardAsTuple, player):
        if self.tp_table_1 == None or self.tp_tbale_neg1 == None:
            return None
        
        if player == 1:
            return self.tp_table_1.getMove(boardAsTuple)
        
        if player == -1:
            return self.tp_tbale_neg1.getMove(boardAsTuple)

class Constants:
    DEFAULT_BOARD_SIZE = 3
    DEFAULT_THREE_D = False
    DEFAULT_VERBOSITY = 1
    DEFAULT_AMOUNT_THREADS = 1
    SYSTEM_VERBOSITY = 0
    PRINT_BOARD_AFTER_EVERY_MOVE = True
    isSimulating = False
    
    #minimax constants
    MAX_DEPTH = 16
    WIN_REWARD = MAX_DEPTH + 1

    #this leads to the directory in which the transposition-table files are stored
    TRANSPOSITION_TABLE_FILE_PATH = "tables/"


    #transposition tables
    GLOBAL_TP_TABLE = TranspositionTable()


        
            



class PlayerTranspositionTable:

    def generateFilePath(directoryPath, boardSize, player): 
        return directoryPath + str(boardSize) + "_" + str(player) + ".pkl"

    def __init__(self, boardSize, player):
        self.boardSize = boardSize  #boardsize of interest this table holds (3 if a 3x3 board is used)
        self.table = {}
        self.player = player 

        self.readTable()

    def readTable(self):
        #initiate table with values from file

        #save a dictionary
        #with open('saved_dictionary.pkl', 'wb') as f:
        #    pickle.dump(self.table, f)
        
        filePath = PlayerTranspositionTable.generateFilePath(Constants.TRANSPOSITION_TABLE_FILE_PATH, self.boardSize, self.player)
        with open(filePath, 'rb') as f:
            self.table = pickle.load(f)
        print()

        
    def getMove(self, boardAsTuple):
        #return the best move and evaluation, if stored in self.table
        if not boardAsTuple in self.table:
            return None
        else:
            return self.table[boardAsTuple]
        

def printToUser(message, message_verbosity, msgWhenSimulating):
    if isAllowedToPrint(message_verbosity, msgWhenSimulating):
        print(message)

def isAllowedToPrint(message_verbosity, msgWhenSimulating):
    if Constants.isSimulating and not msgWhenSimulating:
        #when simulating and the given message is not suppsoed to be printed during simulations, return
        return False
    
    if message_verbosity <= Constants.SYSTEM_VERBOSITY:
        return True
    return False