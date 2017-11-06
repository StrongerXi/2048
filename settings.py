from enum import Enum
import numpy as np



# Board Constants
BOARD_DEFAULT_SIZE = 4
TILE_TWO_PROBABILITY = 0.9
TILE_BASE_VALUE = 2



# Direction Enums
class Direction(Enum):

    up    = "__up__"
    down  = "__down__"
    left  = "__left__"
    right = "__right__"



# Simulation Constants
DEFAULT_NUMBER_OF_STEPS = 3
DEFAULT_SIMULATIONS_IN_EACH_DIRECTION = 10
DEAD_BOARD_PENALTY = -1000

# Evaluator Function Constants
TILE_DIFFERENCE_POWER = 2
TILE_DIFFERENCE_TOLERANCE = 1 ** TILE_DIFFERENCE_POWER
#INTERPRETATION -> DIFFERENCE_TOLERANCE determines the maximum tile difference in terms of log(base_value) raised to diff_power
# that still allows fitness to be positive
# Ex: if tolerance = 3, base value =2,  (16,2), (128,16) would be those edge cases.


"""TILE_WEIGHT_MATRIX = np.array([[16, 12, 8, 5],
                               [12, 10, 6, 3],
                               [8,  6,  4,  2],
                               [5,  3,  2,  1]])"""

TILE_WEIGHT_MATRIX = np.array([[1024, 512, 256, 128],
                               [64, 32, 16, 8],
                               [4,  4,  2,  2],
                               [1,  1,  1,  1]])