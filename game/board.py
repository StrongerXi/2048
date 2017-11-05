import settings
import numpy as np
import random


# This Board Class involves the following:
# -- initialization of Board with optional size given at Board(size)
# -- get and set row/column/tile/board_array
# -- Print out the Board state at Console
# -- Check whether board/tile is moveable at all in any direction
# -- Get the number of empty tiles on board
# -- Check whether the board is moveable in given direction

# Note: Empty Tile is represented as 0
#       All Non-empty Tiles should have positive integer value

class Board():

    def __init__(self,boardsize = settings.BOARD_DEFAULT_SIZE, board = None):

        self.board_size = boardsize
        if board is None:
            self.__board = np.array(Board.initialize_board(self.board_size))
        else:
            self.__board = board




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

    def get_board(self):
        return self.__board


    # Board -> np.array
    # returns a copy of the game board
    def copy_board(self):
        copy = Board()
        copy.__board = np.copy(self.__board)
        return copy


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

    # Board np.Array -> _:
    def set_board(self,board_array):

        for index in range(0,len(self.get_board()[:,0])):
            self.set_row(index,board_array[index])


    # Board -> String
    # Returns the state of the board as a string
    def board_state_string(self):
        bd_string = ""

        for row in self.__board:
            for col in row:
                bd_string += str(col) + "   "
            bd_string += "\n"

        return bd_string

    # Print out the board at console
    def print_board(self):
        print(self.board_state_string())

    # Board -> Boolean
    # Determine if the current board is movable in anydirection
    # if not, return False
    def check_board_moveable(self):
        if self.get_empty_count() != 0:
            return True

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

    def __eq__(self, other):
        if self.board_size != other.board_size:
            raise Exception("error, board sizes do not match for the boards being compared")

        for r in range(0,self.board_size):
            for c in range(0,self.board_size):
                if self.get_tile(r,c) != other.get_tile(r,c):
                    return False

        return True

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


    # Board setting.Direction-> Boolean
    # Checks whether the board is moveable in particular direction
    # If yes, returns True
    # It rotates the board accordingly and applies check-moveable-left to the rotated board
    def check_board_moveable_in_dir(self,dir):

        if dir == settings.Direction.left:
            rotated_board = np.rot90(self.get_board(), 0)
        elif dir == settings.Direction.up:
            rotated_board = np.rot90(self.get_board(), 1)  # transpose
        elif dir == settings.Direction.right:
            rotated_board = np.rot90(self.get_board(), 2)  #
        elif dir == settings.Direction.down:
            rotated_board = np.rot90(self.get_board(), 3)
        else:
            return False

        return Board.check_board_moveable_in_left(rotated_board)

    # np.Array -> Boolean
    # check whether the board is moveable towards the left
    # returns True if it's moveable
    @staticmethod
    def check_board_moveable_in_left(board_array):


        for row in board_array:
            if Board.check_row_moveable_in_left(row):
                return True


        return False

    # Row -> Boolean
    # Check whether the given row is moveable towards the left
    @staticmethod
    def check_row_moveable_in_left(row):

        pivot_tile = row[0]
        has_zero = pivot_tile == 0
        zero_in_between = False

        for index in range(1, row.size):
            current_tile = row[index]

            if current_tile == 0:
                has_zero = True
                continue
            if current_tile == pivot_tile:
                return True

            if has_zero: # This point indicates that current tile is non zero, and differs from pivot
                zero_in_between = True
            pivot_tile = current_tile

        return zero_in_between



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


if __name__ == "__main__":
    bd = Board()

    x = np.array([[0,16,4,2],
                  [2,8,16,4],
                  [8,4,2,16],
                  [4,2,4,8]])

    bd.set_board(x)

    bd.print_board()

    for dir in settings.Direction:
        print(dir, bd.check_board_moveable_in_dir(dir))

