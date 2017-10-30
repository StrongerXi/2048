import settings
import numpy as np
import random


# This Board Class involves the following:
# -- initialization of Board with optional size given at Board(size)
# -- get and set row/column/tile
# -- Print out the Board state at Console
# -- Check whether board/tile is moveable at all in any direction
# -- Get the number of empty tiles on board

# Note: Empty Tile is represented as 0
#       All Non-empty Tiles should have positive integer value

class Board():

    def __init__(self,boardsize = settings.BOARD_DEFAULT_SIZE):

        self.board_size = boardsize

        self.__board = np.array(Board.initialize_board(self.board_size))


    # Board Int Int -> Int/Boolean
    # Return the value of the tile at specified location
    # If given location is out of bounds, return False
    def get_tile(self, row, col):
        if (row < 0 or row >= self.board_size) or \
            (col < 0 or col >= self.board_size):
            return False
        return self.__board[row,col]



    # Board Int -> np.array
    # Return the specified row as a
    def get_row(self,row):
        return self.__board[row,:]

    # Board Int -> np.array
    # Return the specified column as a
    def get_col(self, col):
        return self.__board[:, col]

    def get_board_copy(self):
        copyboard = Board()
        copyboard.set_board(np.copy(self.__board))
        return copyboard

    # Board Int Int NNN -> _
    # Set the specified tile to given value
    def set_tile(self,r,c,value):
        self.__board[r,c] = value

    # Board Int np.Array-> _
    # Set the specified row as input row
    def set_col(self, col_index, input_col):
        target_col = self.get_col(col_index)
        for index in range(0,self.board_size):
            target_col[index] = input_col[index]

    # Board Int np.Array-> _
    # Set the specified row as input row
    def set_row(self, row_index, input_row):
        target_row = self.get_row(row_index)
        for index in range(0,self.board_size):
            target_row[index] = input_row[index]

    def set_board(self,board):
        self.__board = board



    # Print out the board at console
    def print_board(self):
        for row in self.__board:
            for col in row:
                print(col, end = "   ")
            print()

    # Board -> Boolean
    # Determine if the current board is movable in anydirection
    # if not, return False
    def check_board_moveable(self):

        for r in range(0,self.board_size):

            for c in range(r % 2, self.board_size, 2):

                if (self.check_tile_moveable(r, c)):
                    return True

        return False


    # Board Int Int -> Boolean
    # check whether the tile at specified location is moveable
    # meaning, whether it shares identical value with any other vertical or horizontal tiles
    # that are adjacent to it.
    # If not, return False
    def check_tile_moveable(self,row,col):
        target_tile = self.get_tile(row,col)
        for n in range(-1,2,2):

            if self.get_tile(row+n, col) == target_tile or \
               self.get_tile(row, col+n) == target_tile:
                return True

        return False

    # Board -> NNN
    # Returns the number of empty tiles in a Board
    def get_empty_count(self):
        empty_count = 0
        for r in range(0,self.board_size):
            for c in range(0,self.board_size):
                if self.get_tile(r,c) == 0:
                    empty_count += 1

        return empty_count

    def __cmp__(self, other):
        if self.board_size != other.board_size:
            raise Exception("error, board sizes do not match for the boards being compared")

        for r in range(0,self.board_size):
            for c in range(0,self.board_size):
                if self.get_tile(r,c) != other.get_tile(r,c):
                    return -1

        return 0

    # This function generates random tile within the non-empty tiles
    # It first generates a random number within (0, empty-tile-counts)
    # Then it transverses through the board, and each empty tile it encounters
    # reduces the random count by 1, when it's 0 and the current tile is empty
    # it generates a random tile there
    def generate_random_tile(self):

        empty_count = self.get_empty_count()

        if empty_count == 0:
            return

        random_index = random.randint(0, empty_count - 1)

        for r in range(0, self.board_size):
            for c in range(0, self.board_size):

                if self.get_tile(r, c) != 0:
                    continue

                if random_index == 0:
                    if random.uniform(0, 1) < settings.TILE_TWO_PROBABILITY:
                         self.set_tile(r,c,settings.TILE_BASE_VALUE)
                    else:
                         self.set_tile(r,c,settings.TILE_BASE_VALUE * 2)

                random_index -= 1

    # Initialize the game board
    @staticmethod
    def initialize_board(size):
        board = []
        for row in range(0,size):
            r = []
            for col in range(0,size):
                r.append(0)
            board.append(r)
        return board

