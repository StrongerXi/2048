import settings
import unittest
import AI.evaluation
import numpy as np
from game.board import Board

class Evaluation_test(unittest.TestCase):

    def setUp(self):

        self.board1 = np.array(
                          [[1024, 128, 64, 32],
                           [32, 64, 32, 16],
                           [8, 4, 16, 8],
                           [4, 0, 2, 0]])
        self.board2 = np.array(
                          [[1024, 4, 64, 0],
                           [32, 128, 32, 32],
                           [8, 64, 16, 16],
                           [4, 4, 2, 8]])
        self.board3 = np.array([[1024, 128, 64, 32],
                           [32, 64, 32, 16],
                           [8, 4, 16, 8],
                           [2, 4, 0, 2]])

        self.board4 = np.array([[128, 64, 32, 16],
                                [32, 32, 32, 4],
                                [64, 32, 16, 4],
                                [32, 32, 32, 0]])

        self.boards = [Board(board=self.board1),
                       Board(board=self.board2),
                       Board(board=self.board3),
                       Board(board=self.board4)]



    def est_board_evaluation_function(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.board_evaluation_function(board))
            print("\n\n")

    def est_ab_evaluation_function(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.alphabeta_optimized_dir(board,1))
            print("\n\n")

    def test_expectimax_evaluation_function(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.expectimax_optimized_dir(board,1))
            print("\n\n")




unittest.main()