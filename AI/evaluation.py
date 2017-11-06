import settings
import numpy as np
import math
import settings
from game.movement import move_board
import game.board


# Ideas: for size = 4

# TODO: #There should be a penalty for rows such as [256,32,4,0], when the differences are too large
#       # Try creating a dynamic tile/row weight based on the location of largest tile
        #Also, the constants need to be adjusted, and it is suggested that the programmer reads through several
        #entire simulations to identify the reasons that keeps AI from scoring higher
        #Random Simulation stopped moving even though the board is still moveable
        #Need a more comprehensive way for the evaluate board/predict direction function.
        # Maybe list out the possible states for prediction and calculate total fitness with expected individual state fitness

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




# All Functions in this module can take in the Board Object directly.
# A copy would be made within these functions, to ensure that no change would occur
# in the original board being passed in


# Board Number -> Dict-(Direction : Number)
# Input number represents the depth of steps for simulation
# First simulate movement into each direction, then evaluates the board for the board state after
# each directional movement.
# The fitness score of the board state represents the score for each direction.

def evaluate_and_predict_optmized_move(board,steps = 2):

    scores = {settings.Direction.up: 0, settings.Direction.right: 0, settings.Direction.left: 0,
              settings.Direction.down: 0}



    for dir in settings.Direction:

        copy_board = board.copy_board()

        if board.check_board_moveable_in_dir(dir):

            move_score = move_board(copy_board.get_board(), dir)

            board_state_score = deep_evaluate_board_state(copy_board,steps)

            scores[dir] = move_score + board_state_score

        else:
            scores.pop(dir)

    return scores



# Board Number -> Number
# Returns the expected state fitness after having moved a board
# The function generates each possible state by creating 2 and 4 tiles at each empty tile respectively
# and evaluate each one of them.

def deep_evaluate_board_state(board, steps=0):

    if not board.check_board_moveable():
        return settings.DEAD_BOARD_PENALTY

# Past this point, meaning the board is moveable in at least one Direction

    all_possible_state_scores = np.array([],np.int32)

    for row in range(0,board.board_size):

        for col in range(board.board_size):

            if board.get_tile(row,col) == 0:
                state_score = 0
                pop_base_tile_board = board.copy_board()
                pop_base_tile_board.set_tile(row,col,settings.TILE_BASE_VALUE)

                pop_double_base_tile_board = board.copy_board()
                pop_double_base_tile_board.set_tile(row, col, 2*settings.TILE_BASE_VALUE)

                if steps == 0:
                    state_score += settings.TILE_TWO_PROBABILITY * board_evaluation_function(pop_base_tile_board)
                    state_score += (1 - settings.TILE_TWO_PROBABILITY) * board_evaluation_function(pop_double_base_tile_board)

                elif steps > 0:
                    tile_two_deeper_moves_and_scores = evaluate_and_predict_optmized_move(pop_base_tile_board,steps - 1)
                    tile_four_deeper_moves_and_scores = evaluate_and_predict_optmized_move(pop_double_base_tile_board,
                                                                                            steps - 1)
                    tile_two_score = get_highest_score(tile_two_deeper_moves_and_scores)
                    tile_four_score = get_highest_score(tile_four_deeper_moves_and_scores)

                    state_score += tile_two_score + tile_four_score
                else:
                    raise Exception("Steps smaller than zero exeption!")

                all_possible_state_scores = np.append(all_possible_state_scores,state_score)


    return np.median(all_possible_state_scores)



# Board -> Number
# Evaluate the board state's fitness by averaging the fitness for movement in each
# available direction
def evaluate_board_state(board):

    board_copy = board.copy_board()
    board = None

    available_moves = evaluate_available_moves(board_copy)
    max_score = 0
    for key in available_moves:
        max_score = max(max_score, available_moves[key])

    if available_moves:
        return max_score
    else:
        return -1 * sum_board_tiles(board_copy)

"""
    if available_moves:
        average_score = total_score/board.board_size
        return average_score
    else:
        return -1 * sum_board_tiles(board)"""


# Board -> Number
# Sums up all the tiles of given Board
# This negative of this sum will be used as the penalty for a dead state
def sum_board_tiles(board):

    copy_board_state = board.get_board()
    sum = 0

    for r in range(0,len(copy_board_state[:,0])):

        for c in range(0,len(copy_board_state[0,:])):

            sum += copy_board_state[r,c]

    return sum


# Dict-of (Direction : Number) -> Direction
# Find the optimized moves in the given available moves and their evaluation scores
def find_optimized_move(available_moves_scores):

    max_dir = list(available_moves_scores.keys())[0]

    for dir in available_moves_scores:
        if available_moves_scores[dir] > available_moves_scores[max_dir]:
            max_dir = dir

    return max_dir


# Dict-of (Direction : Number) -> Number
# Finds the maximum score in given available_moves_scores

def get_highest_score(available_moves_scores):

    if not available_moves_scores:
        return settings.DEAD_BOARD_PENALTY

    max_score = 0
    for dir in available_moves_scores.keys():
        if available_moves_scores[dir] > max_score:
            max_score = available_moves_scores[dir]

    return max_score




# Board -> Dict-of (setting.Direction : Number)
# This function returns the available direction of movement and their fitness in a dictionary
# although the evaluator function only analyzes the fitness for leftward movement
# This function creates copies of rotated board and evaluate each according, so that all directions are covered
def evaluate_available_moves(board):

    scores = {settings.Direction.up: 0, settings.Direction.right: 0, settings.Direction.left: 0,
              settings.Direction.down: 0}

    for dir in settings.Direction:

        if board.check_board_moveable_in_dir(dir):
            total_tiles = board.get_board().size
            empty_tile_factor = board.get_empty_count()+1/total_tiles
            scores[dir] = board_evaluator_in_dir(board.get_board(), dir) * empty_tile_factor

        else: scores.pop(dir)

    return scores



# Board -> Number
# Evaluate the Board's fitness by:
# 1. Normalize the board value into the power they are raised to(ex. 16 with base 2 would be 4, 8 would be 3...)
# 2. Multiply them with the preset TILE_WEIGHT_MATRIX in settings.py
# 3. Return the sum of the resulted matrix's elements.

def board_evaluation_function(board):


    board_matrix = np.copy(board.get_board())

    for row in range(0,len(board_matrix[:,0])):

        for col in range(0,len(board_matrix[0,:])):

            board_matrix[row,col] = normalize_tile_value(board_matrix[row,col])

    multiplied_matrix = np.multiply(board_matrix, settings.TILE_WEIGHT_MATRIX)

    empty_count_factor = (board.get_empty_count() + 1)/ board.get_board().size



    return np.sum(multiplied_matrix)  * empty_count_factor

# np.Array Direction np.Array -> Number
# Evaluates the fitness for making movement in given direction
# By creating copies of rotated board, and then apply left_evaluator to the board
# The function is able to cover evaluation in any direction
def board_evaluator_in_dir(board, dir, row_weights = np.array([3,2,2,3])):

    if dir == settings.Direction.left:
        rotated_board = np.rot90(board,0)
    elif dir == settings.Direction.up:
        rotated_board = np.rot90(board,1)#transpose
    elif dir == settings.Direction.right:
        rotated_board = np.rot90(board,2)#
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
        #print(row_score)

        row_score *= row_weights[n]

        score += row_score

    return score



# np.Array np.Array-> Number
# Treats the input array vector as a row, and calculate its fitness as if
# it will be moved leftwards. A higher final fitness indicates that this row should be moved
# leftward

def left_row_evaluator(left_row,tiles_weights = np.array([3,2,1])):

    #left_row = drop_zeros(left_row)

    score = 0

    for n in range(0,left_row.size - 1):
        adjacent_tile_score = left_neibor_tiles_evaluator(left_row[n], left_row[n+1])
        adjacent_tile_score *= tiles_weights[n]
        score += adjacent_tile_score

    return score

# np.Array -> np.Array
# Drop all the zeros in given row vector/np.array
def drop_zeros(row_vector):
    zero_indexes = []
    for index in range(0,row_vector.size):
        if row_vector[index] == 0:
            zero_indexes.append(index)

    row_vector = np.delete(row_vector,zero_indexes)

    return row_vector


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
    coef = left_tile + right_tile
    diff_tolerance = settings.TILE_DIFFERENCE_TOLERANCE


    if left_bigger:
        return coef * (diff_tolerance - left_right_diff)
    else:
        return -1 * coef * (diff_tolerance - abs(left_right_diff))


# Number -> Number
# If input number is 0, return 0, else return log of num with preset base
def normalize_tile_value(number):

    if number == 0:
        return 0
    else:
        return math.log(number,settings.TILE_BASE_VALUE)



if __name__ == "__main__":

    bd = game.board.Board()


    board = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [2, 0, 0, 0],
                      [4, 4, 4, 0]])

    for row in range(0,4):
        bd.set_row(row,board[row,:])

    rotboard = np.rot90(board,2)


    #move_board(bd.get_board(),settings.Direction.up)
    bd.print_board()
    #print(evaluate_board_state(bd))
    print(evaluate_available_moves(bd))
    #print(deep_evaluate_board_state(bd))
    print(board_left_evaluator(rotboard))

    print(rotboard)

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


if __name__ == "__main_":

    bd = game.board.Board()
    bd.generate_random_tile()
    bd.print_board()

    print(evaluate_available_moves(bd))

    bd.print_board()
