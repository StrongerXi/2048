import settings
import numpy as np
import math
import settings
from game.movement import move_board
import game.board


# Ideas: for size = 4

# TODO: #There should be a penalty for rows such as [256,32,4,0], when the differences are too large
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





# Board N -> Direction
# A helper function to initiate alpha-beta_deep_evaluate,
# It returns the desired direction after running n levels of simulation
# Assumption: The board is still moveable!
def alphabeta_optimized_dir(board,n):

    best_dir = None
    best_score = -math.inf

    for dir in settings.Direction:
        if board.check_board_moveable_in_dir(dir):

            copy_board = board.copy_board()
            move_score = move_board(copy_board.get_board(),dir)

            score = alphabeta_deep_evaluate(copy_board, 2*n - 1, -math.inf, math.inf, False) + move_score
            #print(score, dir)

            if score > best_score:
                best_score = score
                best_dir = dir


    return best_dir



# Board N Number Number Boolean -> Number
# Board represents a node
# N represents the depth for searching
# Alpha and Beta are Numbers
# Boolean signifies whether it's board/mover's turn
# Returns the direction of the immediate last move and current board score
def alphabeta_deep_evaluate(board, depth, alpha, beta, mover):


    if depth == 0:
        return board_evaluation_function(board)

    if not board.check_board_moveable():
        return settings.DEAD_BOARD_PENALTY

    if not board.max_tile_in_corner():
        return -sum_board_tiles(board)

    if mover:

        potential_higher_alpha = -math.inf

        for dir in settings.Direction:

            if board.check_board_moveable_in_dir(dir):

                new_board_for_move = board.copy_board()

                merge_score = move_board(new_board_for_move.get_board(), dir)

                expected_score = alphabeta_deep_evaluate(new_board_for_move, depth-1, alpha,beta, False)\
                                 + merge_score

                potential_higher_alpha = max(expected_score, potential_higher_alpha)

                alpha = max(alpha,potential_higher_alpha)

                if alpha >= beta:
                    break


        return potential_higher_alpha

    else:

        potential_lower_beta = math.inf

        for index in range(0,board.get_board().size):
            row = index % board.board_size
            col = index // board.board_size
            if board.get_tile(row , col) == 0:

                base_tile_new_board = board.copy_board()
                base_tile_new_board.set_tile(row,col,settings.TILE_BASE_VALUE)
                base_tile_score = alphabeta_deep_evaluate(base_tile_new_board, depth-1, alpha,beta,True)

                combined_weighted_score = settings.TILE_TWO_PROBABILITY * base_tile_score


                double_base_tile_new_board = board.copy_board()
                double_base_tile_new_board.set_tile(row,col,2*settings.TILE_BASE_VALUE)
                double_base_tile_score = alphabeta_deep_evaluate(double_base_tile_new_board, depth-1, alpha,beta,True)

                combined_weighted_score += (1- settings.TILE_TWO_PROBABILITY) * double_base_tile_score

                potential_lower_beta = min(potential_lower_beta, combined_weighted_score)
                beta = min(potential_lower_beta, beta)

                if alpha >= beta:
                    break

        return potential_lower_beta




# Board N -> Direction
# A helper function to initiate Expectimax_deep_evaluate,
# It returns the desired direction after running n levels of simulation
# Assumption: The board is still moveable!
def expectimax_optimized_dir(board, n):

    best_dir = None
    best_score = -math.inf

    for dir in settings.Direction:

        if board.check_board_moveable_in_dir(dir):
            copy_board = board.copy_board()
            move_score = move_board(copy_board.get_board(), dir)

            score = expectimax_deep_evaluate(copy_board, 2*n - 1, False) + move_score
            #print(score, dir)

            if score > best_score:
                best_score = score
                best_dir = dir

    return best_dir


# Board N Boolean -> Number
# Board represents a node
# N represents the depth for searching
# Boolean signifies whether it's board/mover's turn
# Returns the direction of the immediate last move and current board score
def expectimax_deep_evaluate(board, depth, mover):

    if depth == 0:
        return board_evaluation_function(board)

    if not board.check_board_moveable():
        return settings.DEAD_BOARD_PENALTY


    if mover:

        max_score = -math.inf

        for dir in settings.Direction:

            if board.check_board_moveable_in_dir(dir):

                new_board_for_move = board.copy_board()

                merge_score = move_board(new_board_for_move.get_board(), dir)

                expected_score = expectimax_deep_evaluate(new_board_for_move, depth-1, False) \
                                 + merge_score

                max_score = max(max_score, expected_score)


        return max_score

    else:

        sum_of_expected_scores = 0

        for row in range(0,board.board_size):

            for col in range(0,board.board_size):

                if board.get_tile(row, col) == 0:

                    base_tile_new_board = board.copy_board()
                    base_tile_new_board.set_tile(row, col, settings.TILE_BASE_VALUE)

                    base_tile_score = expectimax_deep_evaluate(base_tile_new_board, depth - 1, True)


                    double_base_tile_new_board = board.copy_board()
                    double_base_tile_new_board.set_tile(row, col, 2 * settings.TILE_BASE_VALUE)

                    #double_base_tile_new_board.print_board()

                    double_base_tile_score = expectimax_deep_evaluate(double_base_tile_new_board, depth - 1, True)

                    sum_of_expected_scores += settings.TILE_TWO_PROBABILITY * base_tile_score + \
                                              (1 - settings.TILE_TWO_PROBABILITY) * double_base_tile_score


        return sum_of_expected_scores











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





# Board -> Number
# Evaluate the Board's fitness by:
# 1. Normalize the board value into the power they are raised to(ex. 16 with base 2 would be 4, 8 would be 3...)
# 2. Multiply them with the preset TILE_WEIGHT_MATRIX in settings.py
# 3. Return the sum of the resulted matrix's elements.

def board_evaluation_function(board):

    board_matrix = np.copy(board.get_board())

    """for row in range(0,len(board_matrix[:,0])):

        for col in range(0,len(board_matrix[0,:])):

            board_matrix[row,col] = normalize_tile_value(board_matrix[row,col])"""

    multiplied_matrix = np.multiply(board_matrix, settings.TILE_WEIGHT_MATRIX)

    #empty_count_factor = 1 / (board.get_board().size - board.get_empty_count())
    #print(board.get_empty_count())

    return np.sum(multiplied_matrix) # * empty_count_factor


# np.Array -> np.Array
# Drop all the zeros in given row vector/np.array
def drop_zeros(row_vector):
    zero_indexes = []
    for index in range(0,row_vector.size):
        if row_vector[index] == 0:
            zero_indexes.append(index)

    row_vector = np.delete(row_vector,zero_indexes)

    return row_vector



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
    bd.print_board()

    print(board_evaluation_function(bd))


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

    print("a")
    bd = game.board.Board()
    bd.generate_random_tile()
    bd.print_board()

    bd.print_board()
