import unittest

from game.board import Board

class BoardTest(unittest.TestCase):

    def setUp(self):

        self.board = Board(4)

        self.board.set_row(0, [1, 2, 3, 4])

        self.board.set_row(1, [5, 6, 7, 8])

        self.board.set_row(2, [1, 2, 3, 4])

        self.board.set_row(3, [5, 6, 7, 8])


    def test_check_board_moveable(self):

        self.assertEqual(self.board.check_board_moveable(), False)
        self.board.set_tile(0,0,5)
        self.assertEqual(self.board.check_board_moveable(), True)

    def test_get_empty_count(self):

        self.assertEqual(self.board.get_empty_count(), 0)
        self.board.set_col(0,[1,0,0,1])
        self.assertEqual(self.board.get_empty_count(), 2)
        self.board.set_row(2,[0,0,0,1],)
        self.assertEqual(self.board.get_empty_count(), 4)

    def test_initialize_board(self):

        empty_row = [0,0,0,0,0]

        self.assertEqual(self.board.initialize_board(5), [empty_row, empty_row, empty_row, empty_row, empty_row])

        self.assertEqual(self.board.initialize_board(1), [[0]])

        self.assertEqual(self.board.initialize_board(0), [])

    def test_print_board(self):

        self.board.print_board()


if __name__ == "__main__":
    unittest.main()