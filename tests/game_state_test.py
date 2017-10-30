from tests.board_test_template import BoardTestTemplate
import unittest


class TestGameState(BoardTestTemplate):

    # Because the board is initialized in BoardTestTemplate
    # It's changed here first, then it tests the functionality of initialize_board()
    def test_initialize_board(self):

        filled_row = [1,2,3,4]
        board = []
        for i in range(0,self.gs.size):
            board.append(filled_row)

        init_board = []
        empty_row = [0,0,0,0]
        for i in range(0,self.gs.size):
            init_board.append(empty_row)

        self.gs.initialize_board()
        self.assertEqual(self.gs.board, init_board)

    # Without assertion, this test relies on programmer to determine whether the
    # output is correct
    def print_board(self):
        self.gs.print_board()
        print("aAAa")

    def test_generate_random_tile(self):
        self.gs.board[1][1] = 1
        self.gs.generate_random_tile()
        self.gs.print_board()





if __name__ == '__main__':
    unittest.main()