import settings
import unittest
import AI.evaluation
import numpy as np
from game.board import Board

class Evaluation_test(unittest.TestCase):


    def setUp(self):

        self.board1 = np.array(
                          [[4, 2, 0, 0],
                           [4, 2, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]])
        self.board2 = np.array([[4, 4, 4, 4],
                           [4, 4, 8, 16],
                           [64, 8, 16, 32],
                           [128, 128, 64, 64]])
        self.board3 = np.array([[16, 8, 8, 4],
                           [32, 16, 8, 4],
                           [64, 32, 16, 4],
                           [128, 64, 32, 0]])

        self.boards = [Board(board=self.board1),
                       Board(board=self.board2),
                       Board(board=self.board3)]



    def est_evaluate_available_moves(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.evaluate_available_moves(board))
            print("\n\n")

    def test_deep_evaluate_board_state(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.evaluate_and_predict_optmized_move(board))
            print("\n\n")

    def est_board_evaluator_in_dir(self):
        test_board = self.boards[0]
        test_board.print_board()

        print(AI.evaluation.board_evaluator_in_dir(test_board.get_board(),settings.Direction.down))



unittest.main()