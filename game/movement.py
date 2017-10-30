from enum import Enum
from copy import deepcopy

class Direction(Enum):

    up    = "up"
    down  = "down"
    left  = "left"
    right = "right"


# GameState Direction -> List-of List (game board)
# moves the Game board based on input Direction
def move_board(gs , dir):
    board = deepcopy(gs.board)

    if dir == Direction.up:
        board = move_up(board)
    if dir == Direction.down:
        board = move_down(board)
    if dir == Direction.left:
        board = move_left(board)
    if dir == Direction.right:
        board = move_right(board)

    return board


# List-of List -> List-of List
# Move the gameboard(represented as list of lists -> rows of columns)
# Upwards
def move_up(board):

    bd = deepcopy(board)
    size = len(bd)

    for c in range(0,size):

        # Collects tile values and organize them as a single list
        # as if we will move it leftwards
        this_col = []
        for r in range(0,size):
            this_col.append(bd[r][c])

        # moved the organized list towards left
        # Then copy the values of moved list into bd
        moved_col = move_like_leftrow(this_col)

        for r in range(0,size):
            bd[r][c] = moved_col[r]


    return bd





# List-of List -> List-of List
# Move the gameboard(represented as list of lists -> rows of columns)
# downwards
def move_down(board):

    bd = deepcopy(board)
    size = len(bd)

    for c in range(0, size):

        # Collects tile values and organize them as a single list
        # as if we will move it rightwards
        this_col = []
        for r in range(size-1,-1,-1):
            this_col.append(bd[r][c])

        # moved the organized list towards left
        # Then copy the values of moved list into bd
        moved_col = move_like_leftrow(this_col)

        for r in range(0, size):
            bd[size-1-r][c] = moved_col[r]

    return bd


# List-of List -> List-of List
# Move the gameboard(represented as list of lists -> rows of columns)
# towards the left
def move_left(board):

    bd = board.copy()
    size = len(bd)

    for c in range(0, size):

        moved_row = move_like_leftrow(bd[c])
        bd[c] = moved_row

    return bd


# List-of List -> List-of List
# Move the gameboard(represented as list of lists -> rows of columns)
# towards the right
def move_right(board):

    bd = board.copy()
    size = len(bd)

    for c in range(0, size):
        bd[c].reverse()
        moved_row = move_like_leftrow(bd[c])
        moved_row.reverse()
        bd[c] = moved_row

    return bd


# List -> List
# Treats the numbers in the list as a row
# then move them leftwards
def move_like_leftrow(pseudo_row):

    pseudo_row = move_left_without_merge(pseudo_row)
    pseudo_row = merge_left_row(pseudo_row)
    pseudo_row = move_left_without_merge(pseudo_row)

    return pseudo_row


# List -> List
# Treats the numbers in the list as a row
# then move them leftwards WITHOUT MERGING
# starting from leftmost index, look towards the right for the first
# non-empty tile, then moves that tile to the current index, and set that tile to empty
def move_left_without_merge(pseudo_row):

    row = pseudo_row.copy()
    size = len(row)
    for index in range(0,size):
        if row[index] != 0:
            continue
        for candidate in range(index+1,size):
            if row[candidate] != 0:
                row[index] = row[candidate]
                row[candidate] = 0
                break
    return row


# List -> List
# Treats the numbers in the list as a row
# then merge them towards the left
# This gives priority, to identical and adjacent tiles,
# while reading from the left to right
# PRE-CONDITION: The non-empty tiles in the row must all be located adjacently on the left
# VIOLATION: [2, 0, 2, 0], [0, 2, 2, 2], [2, 2, 0, 2]...
def merge_left_row(pseudo_row):

    row = pseudo_row.copy()
    size = len(pseudo_row)
    index = 1


    while(index < size):
        if row[index] == 0:
            break

        if row[index] == row[index-1]:
            row[index-1] *= 2
            row[index] = 0
            index += 2
        else: index += 1

    return row
