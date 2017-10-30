from game.game_state import GameState
from game.movement import move_board, Direction
import settings

#TODO:
# 1. We need a moved? boolean to determine whether to generate random tiles or not
# 2. The count field should be included in game state
# 3. We need a score field, to keep all the scores
# 4. To accomplish 3 efficiently, we should make movement into a class,
# so that it can access the score field
# Or make it return the obtained score for each move_board
# instead of returning a moved board

class GameRunner():

    def __init__(self):
        self.gs = GameState(settings.BOARD_SIZE)


    def run(self):
        ipt = ""
        self.gs.generate_random_tile()


        while not (ipt == "exit" or self.gs.check_game_over()):

            self.gs.print_board()
            dir = input("please enter 'w' for up, 's' for down, 'a' for left, and 'd' for right, anything else for exit game\n")
            ipt = get_movement(dir)
            self.gs.board = move_board(self.gs, ipt)
            self.gs.generate_random_tile()


        if ipt != "exit":
            print("Sorry, you have lost the game")
            self.gs.print_board()

        else:
            print("why quit, dude?")




def get_movement(dir):
    if dir == "w":
        return Direction.up
    if dir == "s":
        return Direction.down
    if dir == "a":
        return Direction.left
    if dir == "d":
        return Direction.right

    return "exit"






runner = GameRunner()
runner.run()







