
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