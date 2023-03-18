import pickle
from constants import Constants

class TranspositionTable:

    #only want one instance of the transposition table, use initTable() for initiationa nd tpTable as the object.
    tpTable = None
    
    def initTable(boardSize):
        TranspositionTable.tpTable = TranspositionTable()
        TranspositionTable.tpTable.load(boardSize)



    def __init__(self):
        self.tp_table_1 = None
        self.tp_tbale_neg1 = None

        #if false, the table always returns none in the getMoveEvalPair method.
        self.useTable = True

    def load(self, board_size):

        try:
            print("Loading table. Depeding on the table size this could take a few seconds.")

            self.tp_table_1 = PlayerTranspositionTable(boardSize=board_size, player=1)
            self.tp_tbale_neg1 = PlayerTranspositionTable(boardSize=board_size, player=-1)
            print("Finished loading table.")
        except:
            print("Could not load transposition table for board size {0}.".format(board_size))
            self.useTable = False

    def getMoveEvalPair(self, boardAsTuple, player):
        if self.tp_table_1 == None or self.tp_tbale_neg1 == None or not self.useTable:
            return None
        
        if player == 1:
            return self.tp_table_1.getMove(boardAsTuple)
        
        if player == -1:
            return self.tp_tbale_neg1.getMove(boardAsTuple)




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
        
        filePath = PlayerTranspositionTable.generateFilePath(Constants.TRANSPOSITION_TABLE_FILE_PATH, self.boardSize, self.player)
        with open(filePath, 'rb') as f:
            self.table = pickle.load(f)

        
    def getMove(self, boardAsTuple):
        #return the best move and evaluation, if stored in self.table
        if not boardAsTuple in self.table:
            return None
        else:
            return self.table[boardAsTuple]