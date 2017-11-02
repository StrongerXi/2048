import settings
import numpy as np
import math
import settings
import game
from game.movement import move_board
import game.board


# Ideas: for size = 4

# TODO: #Testing for evaluation functions.

# NoTE: The first two coefficients might be the dominant/easier to implement ones
#       It's suggested to implement those first, and observe the simulator's performance.

# Largest tile in corner:
# Count the max tile's distance to closest corner
# Create a penalty/reward coefficient based on that, then multiply the evaluator score.

# Largest tiles are adjacent?:
# Introduces another coefficient.

# Increasing order:
# The number of rows/columns that are in increasing/decreasing order, -> valid for merging
# Bonus if their values are close to each other
# This introduces two more coefficients.




# In the move functions, still calculate the raw score obtained from combining tiles

# Board -> Number
# Evaluate the board state's fitness by averaging the fitness for movement in each
# available direction
def evaluate_board_state(board):

    available_moves = evaluate_available_moves(board)
    total_score = 0
    for key in available_moves:
        total_score += available_moves[key]

    average_score = total_score/len(available_moves)

    return average_score


# Dict-of (Direction : Number)
# Find the optimized moves in the given available moves and their evaluation scores
def find_optimized_move(available_moves_scores):

    max_dir = list(available_moves_scores.keys())[0]

    for dir in available_moves_scores:
        if available_moves_scores[dir] > available_moves_scores[max_dir]:
            max_dir = dir

    return max_dir



# Board -> Dict-of (setting.Direction : Number)
# This function returns the available direction of movement and their fitness in a dictionary
# although the evaluator function only analyzes the fitness for leftward movement
# This function creates copies of rotated board and evaluate each according, so that all directions are covered
def evaluate_available_moves(board):

    scores = {settings.Direction.up: 0, settings.Direction.right: 0, settings.Direction.left: 0,
              settings.Direction.down: 0}

    for dir in settings.Direction:
        move_board(board.copy_board(),dir)
        if not game.movement.moved:
              scores.pop(dir)
        else: scores[dir] = board_evaluator_in_dir(board.get_board(),dir)

    return scores


# np.Array Direction np.Array -> Number
# Evaluates the fitness for making movement in given direction
# By creating copies of rotated board, and then apply left_evaluator to the board
# The function is able to cover evaluation in any direction
def board_evaluator_in_dir(board, dir, row_weights = np.array([2,1,1,2])):

    if dir == settings.Direction.left:
        rotated_board = np.rot90(board,0)
    elif dir == settings.Direction.up:
        rotated_board = np.rot90(board,1)
    elif dir == settings.Direction.right:
        rotated_board = np.rot90(board,2)
    elif dir == settings.Direction.down:
        rotated_board = np.rot90(board,3)
    else:
        raise Exception("Wrong direction input for board_evaluator_in_dir: ",dir, type(dir))

    return board_left_evaluator(rotated_board,row_weights)

# np.Array np.Array  -> Number
# Treats the input n*n array as a board. Evaluate the fitness for moving the board leftward
# The higher the output, the more likely that moving left is the optimized move
def board_left_evaluator(board, row_weights = np.array([1,1,1,1])):

    score = 0

    for n in range(0,board[:,0].size):
        row_score = left_row_evaluator(board[n])
        row_score *= row_weights[n]
        score += row_score

    return score



# np.Array np.Array-> Number
# Treats the input array vector as a row, and calculate its fitness as if
# it will be moved leftwards. A higher final fitness indicates that this row should be moved
# leftward

def left_row_evaluator(left_row,tiles_weights = np.array([3,2,1])):

    score = 0

    for n in range(0,left_row.size - 1):
        adjacent_tile_score = left_neibor_tiles_evaluator(left_row[n], left_row[n+1])
        adjacent_tile_score *= tiles_weights[n]
        score += adjacent_tile_score

    return score


# NNN NNN -> Number
# Treats the left_tile and right_tile as tiles on a row that is about
# to be merged leftward.
# High output score indicates that they favor this leftward move
# Function is maximized with high, and equal tile values.
# It's minimized with high tile value & left-right difference.
# It returns a negative value if right tile is greater than left tile.(This favors move in the opposite -> right direction)
def left_neibor_tiles_evaluator(left_tile,right_tile):


    left_bigger = left_tile >= right_tile

    left_right_diff = (normalize_tile_value(left_tile)- normalize_tile_value(right_tile))
    left_right_diff **= settings.TILE_DIFFERENCE_POWER
    numerator = right_tile


    if left_bigger:
        return numerator / (1 + left_right_diff)
    else:
        return numerator / (1 + abs(left_right_diff)) - right_tile


# Number -> Number
# If input number is 0, return 0, else return log of num with preset base
def normalize_tile_value(number):

    if number == 0:
        return 0
    else:
        return math.log(number,settings.TILE_BASE_VALUE)



if __name__ == "__main__":

    bd = game.board.Board()

    board = np.array([[4, 16, 8, 32],
                      [32, 32, 8, 8],
                      [64, 32, 16, 32],
                      [128, 64, 128, 32]])

    for row in range(0,4):
        bd.set_row(row,board[row,:])

    print(evaluate_board_state(bd))

    """for n in range(0, 4):
        print("\n\n\n")
        temp_board = np.rot90(board, n)
        print(temp_board)
        print(n)
        print(board_left_evaluator(temp_board))

    for dir in settings.Direction:
        print("\n\n\n")
        print(dir)
        print(board_evaluator_in_dir(board,dir))"""

    """row = np.array([4,16,8,32])
    row = row[::-1]
    print(left_row_evaluator(row))"""


    """"   left = 2
    upper_limit = 256

    while left <= upper_limit:

        right = left
        while right <= left * 4:
            print("( ", left, ", ", right, " ) score: ", left_neibor_tiles_evaluator(left,right))
            right *= 2

        left *= 2

    print("over")"""
