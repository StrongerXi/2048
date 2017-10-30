from tests.board_test_template import BoardTestTemplate
from game import movement
import unittest

class MovementTest(BoardTestTemplate):



    def test_move_up(self):
        self.assertEqual(movement.move_up(self.board1), self.up_board1)

    def test_move_down(self):
        self.assertEqual(movement.move_down(self.board1), self.down_board1)

    def test_move_left(self):
        self.assertEqual(movement.move_left(self.board1), self.left_board1)

    def test_move_right(self):
        self.assertEqual(movement.move_right(self.board1), self.right_board1)

    def test_move_like_leftrow(self):
        self.assertEqual(movement.move_like_leftrow([2, 2, 2, 2]), [4, 4, 0, 0])
        self.assertEqual(movement.move_like_leftrow([0, 2, 0, 2]), [4, 0, 0, 0])
        self.assertEqual(movement.move_like_leftrow([2, 0, 2, 2]), [4, 2, 0, 0])

    def test_move_left_without_merge(self):

        self.assertEqual(movement.move_left_without_merge([2, 2, 2, 2]), [2, 2, 2, 2])
        self.assertEqual(movement.move_left_without_merge([0, 2, 0, 2]), [2, 2, 0, 0])
        self.assertEqual(movement.move_left_without_merge([2, 0, 2, 2]), [2, 2, 2, 0])

    def test_merge_left_row(self):

        self.assertEqual(movement.merge_left_row([2, 2, 2, 2]), [4, 0, 4, 0])
        self.assertEqual(movement.merge_left_row([2, 2, 4, 0]), [4, 0, 4, 0])
        self.assertEqual(movement.merge_left_row([4, 2, 2, 0]), [4, 4, 0, 0])
        self.assertEqual(movement.merge_left_row([4, 2, 2]), [4, 4, 0])
        self.assertEqual(movement.merge_left_row([2, 2, 2]), [4, 0, 2])
        self.assertEqual(movement.merge_left_row([2, 2, 4]), [4, 0, 4])


if __name__ == '__main__':
    unittest.main()