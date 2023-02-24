import unittest
from board import Board

#python3 -m unittest -v tests

class BoardTests(unittest.TestCase):

    twod_board = Board(side_length = 3, three_d = False)
    threed_board = Board(side_length = 3, three_d = True)

    def test_2d_win_function(self):
        player = 1
        moveset = [[(0,0), (0,1), (0,2)],
                   [(0,0), (1,1), (2,2)],
                   [(2,0), (2,1), (2,2)],
                   [(2,0), (1,1), (0,2)]]
        for moves in moveset:
            for move in moves:
                BoardTests.twod_board.doMove(move, player)
            self.assertEqual(BoardTests.twod_board.hasWinner(), player)

            BoardTests.twod_board.resetBoard()

    def test_3d_win_function(self):
        player = 1
        moveset =[[(0, 0, 0), (0, 0, 1), (0, 0, 2)],
                    [(1, 0, 0), (1, 0, 1), (1, 0, 2)],
                    [(0, 0, 0), (1, 0, 0), (2, 0, 0)],
                    [(2, 1, 0), (2, 1, 1), (2, 1, 2)],
                    [(2, 1, 0), (2, 1, 1), (2, 1, 2)],
                    [(0, 0, 0), (1, 1, 1), (2, 2, 2)]]
        for moves in moveset:
            for move in moves:
                BoardTests.threed_board.doMove(move, player)

            print("")
            BoardTests.threed_board.printBoard()

            self.assertEqual(BoardTests.threed_board.hasWinner(), player)

            BoardTests.threed_board.resetBoard()

    if __name__ == '__main__':
        unittest.main()
        

