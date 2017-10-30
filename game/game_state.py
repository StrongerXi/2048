import settings
import random
from copy import deepcopy
from game.movement import Direction, move_board

class GameState:

    def __init__(self, size = 4):

        self.size = size
        self.board = self.initialize_board()



    # Initialize the game board
    def initialize_board(self):
        board = []
        for row in range(0,self.size):
            r = []
            for col in range(0,self.size):
                r.append(0)
            board.append(r)
        return board


    # Print out the board at console
    def print_board(self):

        for row in self.board:

            for col in row:
                print(col, end = " ")

            print()


    # This function generates random tile within the non-empty tiles
    # It first generates a random number within (0, empty-tile-counts)
    # Then it transverses through the board, and each empty tile it encounters
    # reduces the random count by 1, when it's 0 and the current tile is empty
    # it generates a random tile there
    def generate_random_tile(self):

        empty_count = self.get_empty_count()

        if empty_count == 0:
            return


        random_index = random.randint(0,empty_count-1)


        for r in range(0,self.size):

            for c in range(0,self.size):

                if self.board[r][c] != 0:
                    continue

                if random_index == 0:
                    if random.uniform(0, 1) < settings.TILE_TWO_PROBABILITY:
                        self.board[r][c] = settings.TILE_BASE_VALUE
                    else:
                        self.board[r][c] = settings.TILE_BASE_VALUE * 2

                random_index -= 1



    def check_game_over(self):

        if self.get_empty_count() != 0:
            return False

        for dir in Direction:
            tempboard = move_board(self,dir)
            # If the board after being moved in any direction is not identical
            # to the original board, game is not over yet
            if not self.identical_board(tempboard):
                return False
        return True



    def identical_board(self,board):

        for r in range(0,self.size):
            for c in range(0,self.size):
                if self.board[r][c] != board[r][c]:
                    return False

        return True


    def get_empty_count(self):
        empty_count = 0
        for r in self.board:
            for c in r:
                if c == 0:
                    empty_count += 1

        return empty_count


