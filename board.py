import random
import numpy as np
import math

class Board:

    EMPTY = 0

    def __init__(self, side_length, three_d=False, initBoard=None):
        if (three_d and initBoard != None):
            raise NotImplementedError("Cannot give initial 3d board. Only 2d.")
        
        self.side_length = side_length
        self.three_d = three_d

        #fields for board
        self.board = []
        self.rotatedBoard = []
        self.rotatedDict = {}   #(i,j,k) : (i', j', k')
        self.inversedRotationDict = {}  #(i', j', k') : (i,j,k) 
        self.emptyFields = []
        if initBoard == None:
            self.initBoardFields()
        else:
            self.board = initBoard
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == Board.EMPTY:
                        self.emptyFields.append((i, j))
            

    def initBoardFields(self):

        self.board = []
        self.rotatedBoard = []
        self.initBoard()

        #dictionary that that converts a cell (i,j,k) into its rotated coordinates (i', j', k') : rotatedDict[(i,j,k)] = (i', j', k')
        #for example :  rotatedDict[(0,0,0)] = (1, 0, 0) - in case of 3x3 
        #the invariant is that borad[(i, j, k)] == rotatedBoard[rotatedDict[(i,j,k)]]

        if self.three_d:
            self.rotatedDict = {}
            self.inversedRotationDict = {}
            self.calculateRotatedCellCoordinates()

        self.emptyFields = [] #todo : initialize correctly
        self.loopOverBoard(lambda i, j, k=-1: self.emptyFields.append((i, j)) if k == -1 else self.emptyFields.append((i,j,k)))
    
    def resetBoard(self):
        self.initBoardFields()

    def initBoard(self):
        #initialize baord with all EMPTY fields
        if self.three_d:
            for i in range(self.side_length):
                plane = []
                rotatedPlane = []
                for j in range(self.side_length):
                    plane.append([Board.EMPTY for k in range(self.side_length)])
                    rotatedPlane.append([Board.EMPTY for k in range(self.side_length)])

                self.board.append(plane)
                self.rotatedBoard.append(rotatedPlane)

            
        else:
            for i in range(self.side_length):
                self.board.append([Board.EMPTY for j in range(self.side_length)])

    def calculateRotatedCellCoordinates(self):
        """
        When we look at the array as each index (i,j,k) were coordinates, every cell in the array corresponds to a single 
        point in a coordiante system. And the cube itself has only length (self.side_lengt - 1).
        """
        translation_vector = np.array([
            (self.side_length-1) / 2, 0, (self.side_length-1) / 2   
        ])
        rotation_matrix = np.array([
            [0,0,1],
            [0,1,0],
            [-1,0,0]
        ])  #rotation matrix for rotation around y-axis with 90°


        

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                for k in range(len(self.board[i][j])):
                    
                    cell = np.array([i,j,k])
                    #shifting the cell in the xz-plane, such that the y-axis is the center of the cube 
                    shifted_cell = cell - translation_vector
                    #rotate the cell around the y-axis
                    rotated_cell = np.dot(rotation_matrix, shifted_cell)
                    
                    #shift the point back as if it was rotated around the axis of the cubes center
                    #in case of odd dimensions (e.g. 3, all points besides)
                    translatedPoint = np.floor(rotated_cell + translation_vector)
                    rotated_cell_coordinates = (int(translatedPoint[0]),int(translatedPoint[1]), int(translatedPoint[2]))
                    self.rotatedDict[(i,j,k)] = rotated_cell_coordinates
                    #self.rotatedDict[(i,j,k)] = (translatedPoint[0] , translatedPoint[1],  translatedPoint[2])
                    self.inversedRotationDict[rotated_cell_coordinates] = (i,j,k)


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

        if self.three_d:

            """
                for plane, planeRotated in zip(self.board, self.rotatedBoard):
                winner = self.check2dBoard_forWinner(plane)
                winner_r = self.check2dBoard_forWinner(planeRotated)
                if (winner != 0):
                    return winner
                if (winner_r != 0):
                    return winner_r


            #still have to check cube diagonals - IF board dimension is odd!
            if not (self.side_length % 2 == 0):
                diagsums = [0,0,0,0]
                for i in range(self.side_length):
                    diagsums[0] += self.board[i][i][i]
                    diagsums[1] += self.board[self.side_length - 1 - i][self.side_length - 1 - i][i]
                    diagsums[2] += self.board[self.side_length - 1 - i][i][self.side_length - 1 - i]
                    diagsums[3] += self.board[i][self.side_length - 1 - i][self.side_length - 1 - i]
                
                for diagsum in diagsums:
                    if (abs(diagsum) == self.side_length):
                        return int(diagsum / self.side_length)"""
            allSlices = self.getAllSlices()
            for slice in allSlices:
                winner = self.check2dBoard_forWinner(slice)
                if (winner != 0):
                    return winner

            return 0

            
            #after that : rotate the whole tic tac toe cube by 90 degrees, such that the forward facing plane is now on the left side (or right side) of the cube
            #check all three planes agian

            #check the cube diagonals
        else:
            return self.check2dBoard_forWinner(self.board)

    def check2dBoard_forWinner(self, two_dboard):
        #return [-1, 1] if 1 or -1 won on this twod_board and 0 if there is no winner
        dim = len(two_dboard)
        diagonal1_sum = diagonal2_sum = 0
        for i in range(dim):
            rowsum = columnsum = 0
            for j in range(dim):
                #rows
                rowsum += two_dboard[i][j]

                #cols
                columnsum += two_dboard[j][i]

            if abs(rowsum) == dim:
                return int (rowsum / dim)
            if abs(columnsum) == dim:
                return int (columnsum / dim) 
            
            diagonal1_sum += two_dboard[i][i]  #0, 4, 8
            diagonal2_sum += two_dboard[i][dim - 1 - i] #2, 4, 6
        if abs(diagonal1_sum) == dim:
            return int (diagonal1_sum / dim)
        if abs(diagonal2_sum) == dim:
            return int (diagonal2_sum / dim)
        return 0 



    def setIcon(self, icon, move):

        if self.three_d:
            x,y,z = move[0], move[1], move[2]
            self.board[x][y][z] = icon

            #keep the rotated board updated
            rotated_coords = self.rotatedDict[move]
            self.rotatedBoard[rotated_coords[0]][rotated_coords[1]][rotated_coords[2]] = icon
        else:
            x, y = move[0], move[1]
            self.board[x][y] = icon

    def doMove(self, move, player):
        #places player into the index described by move
        #keep live update of possible moves in self.emptyFields and self.hasMoves

        self.setIcon(player, move)

        #update empty fields
        self.emptyFields.remove(move)
        

    def undoMove(self, move):
        self.setIcon(Board.EMPTY, move)
        self.emptyFields.append(move)
    
    def isEmptyAt(self, cell):
        if self.three_d:
            return self.board[cell[0]][cell[1]][cell[2]] == Board.EMPTY
        else:
            return self.board[cell[0]][cell[1]] == Board.EMPTY

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
    
    def getSlice(self, plane_index, rotated, angled=0):
        if not self.three_d:
            return self.board.copy()
        
        if angled == 1:
            #angled is ignored until now
            angledBoard = []
            for i in range(self.side_length):
                angledRow = []
                for j in range(self.side_length):
                    angledRow.append(self.board[i][j][j])
                angledBoard.append(angledRow)
            return angledBoard
        if angled == 2:
            angledBoard = []
            for i in range(self.side_length):
                angledRow = []
                for j in range(self.side_length):
                    angledRow.append(self.board[i][self.side_length - 1 - j][j])
                angledBoard.append(angledRow)
            return angledBoard
            

        #3d case
        if not rotated:
            return self.board[plane_index].copy()
        else:
            return self.rotatedBoard[plane_index].copy()

    def getAllSlices(self):
        if not self.three_d:
            return [self.board]
        #3d case
        slices = []
        for i in range(self.side_length):
            slices.append(self.getSlice(i, rotated=False))
        for i in range(self.side_length):
            slices.append(self.getSlice(i, rotated=True))

        #rotated slices not implemented yet, even if self.side_length not odd, there have to be two
        #boards for cube diagonals
        slices.append(self.getSlice(0, rotated=False, angled=1))    #no other parametrs matter if angled != 0
        slices.append(self.getSlice(0, rotated=False, angled=2))
        return slices
    
    def getTuple(self):
        if self.three_d:
            pass
        else:
            return tuple(map(tuple, self.board.copy()))

