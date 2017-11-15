
import sys
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))
#set cwd to directory of current module(evaluation_test), which is ......2048/tests/
sys.path.append(os.path.abspath(os.curdir) + "/..") # Add 2048 to sys.path so that settings.py could be accessed

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

        self.boards = []

        """[Board(board=self.board1),
                       Board(board=self.board2),
                       Board(board=self.board3),
                       Board(board=self.board4)]"""

        self.read_matrix_from_data(1)


    def est_a(self):
        pass

    def est_board_evaluation_function(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.board_evaluation_function(board))
            print("\n\n")

    def test_ab_evaluation_function(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.alphabeta_optimized_dir(board,3))
            print("\n\n")

    def est_expectimax_evaluation_function(self):

        for board in self.boards:
            board.print_board()
            print(AI.evaluation.expectimax_optimized_dir(board,3))
            print("\n\n")


    # Board NNN -> Numpy.Array
    # Read n Numpy.Array from the data_transition_file
    # and add them to the self.boards
    def read_matrix_from_data(self,n):

        data = open("data_transition_file",'r')

        for i in range(0,n):

            list_of_rows = []

            for r in range(0,4):
                l = list(map(int,data.readline().split()))
                list_of_rows.append(l)

            data.readline()

            bs = np.array(list_of_rows)

            board = Board(board = bs)
            self.boards.append(board)

        data.close()




unittest.main()
