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
        self.board2 = np.array([[0, 64, 8, 4],
                           [0, 0, 0, 4],
                           [0, 4, 0, 4],
                           [0, 0, 0, 4]])
        self.board3 = np.array([[64, 8, 4, 0],
                           [4, 0, 0, 0],
                           [4, 0, 0, 0],
                           [2, 0, 2, 0]])

        self.board4 = np.array([[128, 64, 32, 16],
                                [32, 32, 32, 4],
                                [64, 32, 16, 4],
                                [32, 32, 32, 0]])

        self.boards = [Board(board=self.board1),
                       Board(board=self.board2),
                       Board(board=self.board3),
                       Board(board=self.board4)]



    def est_evaluate_available_moves(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.evaluate_available_moves(board))
            print("\n\n")

    def est_deep_evaluate_board_state(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.evaluate_and_predict_optmized_move(board))
            print("\n\n")

    def est_board_evaluator_in_dir(self):
        test_board = self.boards[0]
        test_board.print_board()

        print(AI.evaluation.board_evaluator_in_dir(test_board.get_board(),settings.Direction.down))

    def test_board_evaluation_function(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.board_evaluation_function(board))
            print("\n\n")




unittest.main()