import random
import numpy as np
import math

class Board:

    EMPTY = 0

    def __init__(self, side_lengh, three_d=False):
        self.side_length = side_lengh
        self.three_d = three_d

        self.board = []
        self.rotatedBoard = []
        self.initBoard()

        #dictionary that that converts a cell (i,j,k) into its rotated coordinates (i', j', k') : rotatedDict[(i,j,k)] = (i', j', k')
        #for example :  rotatedDict[(0,0,0)] = (1, 0, 0) - in case of 3x3 
        #the invariant is that borad[(i, j, k)] == rotatedBoard[rotatedDict[(i,j,k)]]

        self.rotatedDict = {}
        self.calculateRotatedCellCoordinates()

        self.emptyFields = [] #todo : initialize correctly
        self.loopOverBoard(lambda i, j, k=-1: self.emptyFields.append((i, j)) if k == -1 else self.emptyFields.append((i,j,k)))

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
        translation_vector = np.array([
            math.floor(self.side_length) / 2, 0, math.floor(self.side_length / 2)
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

                    self.rotatedDict[(i,j,k)] = (int(translatedPoint[0]),int(translatedPoint[1]), int(translatedPoint[2]))
                    #self.rotatedDict[(i,j,k)] = (translatedPoint[0] , translatedPoint[1],  translatedPoint[2])


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
            for plane in range(len(self.board)):
                winner = self.check2dBoard_forWinner(self.board[plane])
                if (winner != 0):
                    return winner
            
            #after that : rotate the whole tic tac toe cube by 90 degrees, such that the forward facing plane is now on the left side (or right side) of the cube
            #check all three planes agian

            #check the cube diagonals
        else:
            return self.check2dBoard_forWinner(self.board)

    def check2dBoard_forWinner(self, two_dboard):
        #return [-1, 1] if 1 or -1 won on this twod_board and 0 if there is no winner
        for i in range(len(two_dboard)):
            for j in range(len(two_dboard)):

                pass



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

    def doMove(self, player,  move):
        #places player into the index described by move
        #keep live update of possible moves in self.emptyFields and self.hasMoves

        self.setIcon(player, move)

        #update empty fields
        self.emptyFields.remove(move)
        

    def undoMove(self, move):
        self.setIcon(Board.EMPTY, move)
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

board = Board(side_lengh=3, three_d=True)
print(board.rotatedDict)