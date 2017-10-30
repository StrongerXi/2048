from game.game_state import GameState
import unittest


class BoardTestTemplate(unittest.TestCase):

    def setUp(self):
        self.gs = GameState()
        self.gs.initialize_board()

        self.board1 = [[2, 2, 2, 2],
                  [2, 0, 2, 2],
                  [0, 2, 2, 2],
                  [4, 2, 2, 2]]

        self.left_board1 = [[4, 4, 0, 0],
                       [4, 2, 0, 0],
                       [4, 2, 0, 0],
                       [4, 4, 2, 0]]

        self.right_board1 = [[0, 0, 4, 4],
                        [0, 0, 2, 4],
                        [0, 0, 2, 4],
                        [0, 4, 2, 4]]

        self.up_board1 = [[4, 4, 4, 4],
                     [4, 2, 4, 4],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]

        self.down_board1 = [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [4, 2, 4, 4],
                       [4, 4, 4, 4]]
