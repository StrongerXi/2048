from game.board import Board
from game import movement
import unittest

class MovementTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.set_row(0, [2, 2, 2, 2])
        self.board.set_row(1, [0, 2, 4, 2])
        self.board.set_row(2, [2, 4, 2, 2])
        self.board.set_row(3, [0, 2, 2, 4])

        self.up_board = Board()
        self.up_board.set_row(0, [4, 4, 2, 4])
        self.up_board.set_row(1, [0, 4, 4, 2])
        self.up_board.set_row(2, [0, 2, 4, 4])
        self.up_board.set_row(3, [0, 0, 0, 0])

        self.down_board = Board()
        self.down_board.set_row(0, [0, 0, 0, 0])
        self.down_board.set_row(1, [0, 4, 2, 2])
        self.down_board.set_row(2, [0, 4, 4, 4])
        self.down_board.set_row(3, [4, 2, 4, 4])

        self.left_board = Board()
        self.left_board.set_row(0, [4, 4, 0, 0])
        self.left_board.set_row(1, [2, 4, 2, 0])
        self.left_board.set_row(2, [2, 4, 4, 0])
        self.left_board.set_row(3, [4, 4, 0, 0])

        self.right_board = Board()
        self.right_board.set_row(0, [0, 0, 4, 4])
        self.right_board.set_row(1, [0, 2, 4, 2])
        self.right_board.set_row(2, [0, 2, 4, 4])
        self.right_board.set_row(3, [0, 0, 4, 4])

    def test_move_up(self):
        self.assertEqual(movement.move_up(self.board), 16)
        self.assertEqual(self.board, self.up_board)

    def test_move_down(self):
        self.assertEqual(movement.move_down(self.board), self.down_board)

    def test_move_left(self):
        self.assertEqual(movement.move_left(self.board), self.left_board)

    def test_move_right(self):
        self.assertEqual(movement.move_right(self.board), self.right_board)

    def est_move_like_leftrow(self):
        self.assertEqual(movement.move_like_leftrow([2, 2, 2, 2]), [4, 4, 0, 0])
        self.assertEqual(movement.move_like_leftrow([0, 2, 0, 2]), [4, 0, 0, 0])
        self.assertEqual(movement.move_like_leftrow([2, 0, 2, 2]), [4, 2, 0, 0])

    def est_move_left_without_merge(self):

        self.assertEqual(movement.move_left_without_merge([2, 2, 2, 2]), [2, 2, 2, 2])
        self.assertEqual(movement.move_left_without_merge([0, 2, 0, 2]), [2, 2, 0, 0])
        self.assertEqual(movement.move_left_without_merge([2, 0, 2, 2]), [2, 2, 2, 0])

    def est_merge_left_row(self):

        self.assertEqual(movement.merge_left_row([2, 2, 2, 2]), [4, 0, 4, 0])
        self.assertEqual(movement.merge_left_row([2, 2, 4, 0]), [4, 0, 4, 0])
        self.assertEqual(movement.merge_left_row([4, 2, 2, 0]), [4, 4, 0, 0])
        self.assertEqual(movement.merge_left_row([4, 2, 2]), [4, 4, 0])
        self.assertEqual(movement.merge_left_row([2, 2, 2]), [4, 0, 2])
        self.assertEqual(movement.merge_left_row([2, 2, 4]), [4, 0, 4])


if __name__ == '__main__':
    unittest.main()