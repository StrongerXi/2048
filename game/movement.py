from enum import Enum
from copy import deepcopy

# This Class Involves the following:
# - Direction Enum for moving the board
# - Move board in any Direction
# - Helper functions that move/merge row/column

# Note:
#       - The functions in this module must take in a Board Class

moved = False

class Direction(Enum):

    up    = "up"
    down  = "down"
    left  = "left"
    right = "right"


# Board Direction -> List-of List (game board)
#  The move_board function returns the merging score based on rules of the game
#  If movement in a direction is ineffective, move_board returns 0
def move_board(board , dir):

    global moved
    moved = False

    score = 0

    if dir == Direction.up:
        score = move_up(board)
    if dir == Direction.down:
        score = move_down(board)
    if dir == Direction.left:
        score = move_left(board)
    if dir == Direction.right:
        score = move_right(board)


    return score




# Board -> NNN
# Move the Board upwards and return the score obtained from
# any merged tiles
def move_up(board):

    score = 0

    size = board.board_size

    for c in range(0,size):

        # Collects each coloumn as a [c0,c1,c2....] array,
        # then move it leftwards(effectively same as moving upward with a column vector)
        this_col = board.get_col(c)
        # Add the score attained from this single column move to total score
        score += move_like_leftrow(this_col)


    return score


# Board -> NNN
# Move the Board downwards and return the score obtained from
# any merged tiles
def move_down(board):
    score = 0


    size = board.board_size

    for c in range(0, size):
        # Collects each coloumn as a [c0,c1,c2....] array,
        # then reverses it, moves reversed array rightward, then reverse it again
        # (effectively same as moving upward with a column vector)
        this_col = board.get_col(c)
        reversed_col = this_col[::-1] # First reverse
        # Add the score attained from this single column move to total score
        score += move_like_leftrow(reversed_col)
        #board.set_col(c, reversed_col[::-1])  # Reverse back and set the column on board

    return score


# Board -> NNN
# Move the Board leftward and return the score obtained from
# any merged tiles
def move_left(board):
    score = 0


    size = board.board_size

    for r in range(0, size):
        # Collects each row as a [c0,c1,c2....] array,\
        # then move it leftward
        this_row = board.get_row(r)
        # Add the score attained from this single column move to total score
        score += move_like_leftrow(this_row)

    return score

# Board -> NNN
# Move the Board downwards and return the score obtained from
# any merged tiles
def move_right(board):
    score = 0
    size = board.board_size

    for r in range(0, size):
        # Collects each row as a [c0,c1,c2....] array,
        # then reverses it, and moves the reversed array.
        this_row = board.get_row(r)
        reversed_col = this_row[::-1] # First reverse
        # Add the score attained from this single column move to total score
        score += move_like_leftrow(reversed_col)
        #board.set_col(c, reversed_col[::-1])  # Reverse back and set the column on board

    return score


# np.Array -> NNN
# Treats the numbers in the list as a row
# then move them leftwards
def move_like_leftrow(pseudo_row):

    move_left_without_merge(pseudo_row)
    score = merge_left_row(pseudo_row)
    move_left_without_merge(pseudo_row)

    return score


# List -> List
# Treats the numbers in the list as a row
# then move them leftwards WITHOUT MERGING
# starting from leftmost index, look towards the right for the first
# non-empty tile, then moves that tile to the current index, and set that tile to empty
def move_left_without_merge(pseudo_row):

    size = pseudo_row.size

    for index in range(0,size):
        if pseudo_row[index] != 0:
            continue
        for candidate in range(index+1,size):
            if pseudo_row[candidate] != 0:
                pseudo_row[index] = pseudo_row[candidate]
                pseudo_row[candidate] = 0
                global moved
                moved = True

                break


# List -> List
# Treats the numbers in the list as a row
# then merge them towards the left
# This gives priority, to identical and adjacent tiles,
# while reading from the left to right
# PRE-CONDITION: The non-empty tiles in the row must all be located adjacently on the left
# VIOLATION: [2, 0, 2, 0], [0, 2, 2, 2], [2, 2, 0, 2]...
def merge_left_row(pseudo_row):

    score = 0
    size = pseudo_row.size
    index = 1

    while(index < size):
        if pseudo_row[index] == 0:
            break

        if pseudo_row[index] == pseudo_row[index-1]:

            pseudo_row[index-1] *= 2
            pseudo_row[index] = 0
            score = pseudo_row[index-1]

            global moved
            moved = True

            index += 2
        else: index += 1

    return score
