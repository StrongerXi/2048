
from game.board import Board

class GameState:

    def __init__(self, size = 4):

        self.size = size
        self.board = Board()
        self.__score = 0


    def add_score(self, score_to_add):

        self.__score += score_to_add


    def get_score(self):

        return self.__score


    def reset(self):
        self.__init__()



gs = GameState()

gs.board.set_tile(2,2,2)

gs.board.print_board()

gs.reset()

gs.board.print_board()