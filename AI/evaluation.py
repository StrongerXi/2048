import settings


# Ideas: for size = 4

# TODO:

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
