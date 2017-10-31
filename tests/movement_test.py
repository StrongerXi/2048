from game.board import Board
from game import movement
import numpy as np
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

        self.likerow1 = np.array([2, 2, 2, 2])
        self.likerow1moved = np.array([4, 4, 0, 0])
        self.likerow1notmerged = np.array([2,2,2,2])
        self.likerow1merged = np.array([4, 0, 4, 0])

        self.likerow2 = np.array([0, 2, 0, 2])
        self.likerow2moved = np.array([4, 0, 0, 0])
        self.likerow2notmerged = np.array([2,2,0,0])

        self.likerow3 = np.array([2, 0, 2, 2])
        self.likerow3moved = np.array([4, 2, 0, 0])
        self.likerow3notmerged = np.array([2,2,2,0])

        self.likerow4 = np.array([2, 2, 4, 0])
        self.likerow4moved = np.array([4, 4, 0, 0])
        self.likerow4merged = np.array([4, 0, 4, 0])
        self.likerow4notmerged = np.array([2,2,4,0])

    def test_move_up(self):
        self.assertEqual(movement.move_up(self.board), 16)
        self.assertEqual(self.board, self.up_board)

    def test_move_down(self):
        self.assertEqual(movement.move_down(self.board), 16)
        self.assertEqual(self.board, self.down_board)

    def test_move_left(self):
        self.assertEqual(movement.move_left(self.board), 16)
        self.assertEqual(self.board, self.left_board)

    def test_move_right(self):
        self.assertEqual(movement.move_right(self.board), 16)
        self.assertEqual(self.board, self.right_board)

    def test_move_like_leftrow(self):
        movement.move_like_leftrow(self.likerow1)
        self.assertEqual(self.likerow1.tolist(), self.likerow1moved.tolist())
        movement.move_like_leftrow(self.likerow2)
        self.assertEqual(self.likerow2.tolist(), self.likerow2moved.tolist())
        movement.move_like_leftrow(self.likerow3)
        self.assertEqual(self.likerow3.tolist(), self.likerow3moved.tolist())
        movement.move_like_leftrow(self.likerow4)
        self.assertEqual(self.likerow4.tolist(), self.likerow4moved.tolist())


    def test_move_left_without_merge(self):

        movement.move_left_without_merge(self.likerow1)
        self.assertEqual(self.likerow1.tolist(), self.likerow1notmerged.tolist())
        movement.move_left_without_merge(self.likerow2)
        self.assertEqual(self.likerow2.tolist(), self.likerow2notmerged.tolist())
        movement.move_left_without_merge(self.likerow3)
        self.assertEqual(self.likerow3.tolist(), self.likerow3notmerged.tolist())
        movement.move_left_without_merge(self.likerow4)
        self.assertEqual(self.likerow4.tolist(), self.likerow4notmerged.tolist())

    def test_merge_left_row(self):


        self.assertEqual(movement.merge_left_row(self.likerow1), 8)
        self.assertEqual(self.likerow1.tolist(), self.likerow1merged.tolist())
        self.assertEqual(movement.merge_left_row(self.likerow4), 4)
        self.assertEqual(self.likerow4.tolist(), self.likerow4merged.tolist())



if __name__ == '__main__':
    unittest.main()