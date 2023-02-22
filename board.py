import random

class Board:

    EMPTY = 0

    def __init__(self, side_lengh, three_d=False):
        self.side_length = side_lengh
        self.three_d = three_d

        self.board = []
        #create array
        if self.three_d:
            for i in range(self.side_length):
                plane = []
                for j in range(self.side_length):
                    plane.append([0 for i in range(self.side_length)])
                self.board.append(plane)
        else:
            for i in range(self.side_length):
                self.board.append([0 for i in range(self.side_length)])



        self.emptyFields = [] #todo : initialize correctly
        self.loopOverBoard(lambda i, j, k=-1: self.emptyFields.append((i, j)) if k == -1 else self.emptyFields.append((i,j,k)))
        

    def loopOverBoard(self, function):
        if self.three_d:
            for i in range(self.side_length):
                    for j in range(self.side_length):
                        for k in range(self.side_length):
                            function(i, j, k)
        else:
            for i in range(self.side_length):
                for j in range(self.side_length):
                    function(i, j)
    
    def hasMoves(self):
        #return true if there are empty fields left on the board
        return len(self.emptyFields) > 0

    def getPossibleMoves(self):
        #returns an array of touples (i, j) or (i,j,k) depending on the dimension of the board where it is possible to move
        #create deep-copy of self.emptyfields

        emptyFieldsCopy =[]
        for move in self.emptyFields:
            emptyFieldsCopy.append(move)
        return emptyFieldsCopy
    
    def getRandomPossibleMove(self):
        return self.emptyFields[random.randint(0, len(self.emptyFields) - 1)]

    
    def hasWinner(self):
        # return [1, -1] if either of these two is the winner, 0 if there is no winner
        pass


    def setPlayerIcon(self, player, move):

        if self.three_d:
            x,y,z = move[0], move[1], move[2]
            self.board[x][y][z] = player
        else:
            x, y = move[0], move[1]
            self.board[x][y] = player

    def doMove(self, player,  move):
        #places player into the index described by move
        #keep live update of possible moves in self.emptyFields and self.hasMoves

        self.setPlayerIcon(player, move)

        #update empty fields
        self.emptyFields.remove(move)
        

    def undoMove(self, move):
        self.setPlayerIcon(Board.EMPTY, move)
        self.emptyFields.append(move)

    def printBoard(self):
        
        if self.three_d:
            three_d_stringArray = []
            distance_between_planes = "          "
            for plane in range(len(self.board)):
                if (plane == 0):
                    three_d_stringArray = self.get2dStringArray(self.board[plane])
                else:
                    #for threed_String, twod_String in zip(three_d_stringArray, self.get2dStringArray(self.board[plane])):
                    for index_3d, twod_String in enumerate(self.get2dStringArray(self.board[plane])):
                        three_d_stringArray[index_3d] += distance_between_planes + twod_String

            stringArray = three_d_stringArray
        else:
            #in 2d case this means just printig each row-stirng of the stringarray
            stringArray = self.get2dStringArray(self.board)

        for string in stringArray:
            print(string)

    def get2dStringArray(self, two_d_array):
        #basically returns an array of strings, where each entry represents one line to be printed 
        stringarray = []
        for i in range(len(two_d_array)):
            rowString  = ""
            for j in range(len(two_d_array[i])):
                c = two_d_array[i][j]
                rowString +=  "{:^3}".format(c)
                if (j < len(two_d_array[i]) - 1):
                    rowString += " | "
            stringarray.append(rowString)
        return stringarray

board = Board(side_lengh=5, three_d=True)
board.printBoard()
