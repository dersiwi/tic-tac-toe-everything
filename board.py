
class Board:

    def __init__(self, side_lengh, three_d=False):
        self.side_length = side_lengh
        self.three_d = three_d

        self.board = []
        #create array
        if self.three_d:
            for i in range(self.side_length):
                for j in range(self.side_length):
                    self.board.append([0 for i in range(self.side_length)])
        else:
            for i in range(self.side_length):
                self.board.append([0 for i in range(self.side_length)])