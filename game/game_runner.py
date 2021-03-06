from game.game_state import GameState
from game.movement import move_board
import settings
from AI import evaluation


#TODO:
# 1. The game_runner uses the moved global variable from movement module
#    This module might need to be changed into a movement class
#    So that multiple module/classes could access movement class and has
#    Their own moved instance, instead of relying on only one



class GameRunner():

    def __init__(self,gamestate = GameState(settings.BOARD_DEFAULT_SIZE)):

        self.gs = gamestate

        self.board = self.gs.board


    def run(self):
        ipt = ""
        self.board.generate_random_tile()

        while  (ipt != "exit" and self.board.check_board_moveable()):

            print("\n\ncurrent score: ", self.gs.get_score())
            self.board.print_board()
            print("\n predict optimized move: ", evaluation.evaluate_and_predict_optmized_move(self.board))
            print("\n available moves",evaluation.evaluate_available_moves(self.board))

            dir = input("\nplease enter 'w' for up, 's' for down, 'a' for left, and 'd' for right, anything else for exit game\n")
            ipt = get_movement(dir)

            if self.board.check_board_moveable_in_dir(ipt):
                round_score = move_board(self.board.get_board(), ipt)
                self.board.generate_random_tile()
                self.gs.add_score(round_score)


        if ipt != "exit":
            print("Sorry, you have lost the game")
            self.board.print_board()

        else:
            print("why quit, dude?")




def get_movement(dir):
    if dir == "w":
        return settings.Direction.up
    if dir == "s":
        return settings.Direction.down
    if dir == "a":
        return settings.Direction.left
    if dir == "d":
        return settings.Direction.right

    return "exit"



if __name__ == "__main__":

    runner = GameRunner()
    runner.run()






