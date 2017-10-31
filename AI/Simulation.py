
from game.game_state import GameState
from game.movement import Direction, move_board
import game.movement

import settings


class Simulation:

    def __init__(self):

        self.gs = GameState()
        self.board = self.gs.board
        self.board.generate_random_tile()


    # NNN NNN NNN -> Void
    # Rounds represent the number of simulations desired
    # num_of_steps represents the number of steps wanted into each direction
    # sim_in_dir represents the number of random movements wanted after going into one direction

    # A single simulation breaks when:
    #

    def random_simulator(self,rounds, num_of_steps = settings.DEFAULT_NUMBER_OF_STEPS, sim_in_dir = settings.DEFAULT_SIMULATIONS_IN_EACH_DIRECTION):

        simFlag = True

        while simFlag:

            if not self.board.check_board_moveable():
                simFlag = False
                break

            self.board.print_board()
            print("score: ", self.gs.get_score(), "\n\n\n")

            optimizedDir = self.random_simulate(num_of_steps, sim_in_dir)
            round_score = move_board(self.board, optimizedDir)
            self.board.generate_random_tile()
            self.gs.add_score(round_score)

        self.board.print_board()






    # Simulation  -> Direction
    # This Function finds the optimized move by first moving in each direction
    # Then it randomly generates moves from that point, based on
    #   - num_of_steps
    #   - sims_in_each_dir
    # It returns the direction that yields the best average score
    def random_simulate(self, num_of_steps, sim_in_dir):

        scores = {Direction.up: 0, Direction.right: 0, Direction.left: 0, Direction.down: 0}

        for dir in Direction:

            scores[dir] += self.random_simulate_in_direction(dir, num_of_steps, sim_in_dir)

        max_dir = Direction.up

        for dir in Direction:
            if scores[dir] > scores[max_dir]:
                max_dir = dir
            print(dir, scores[dir])


        return max_dir


    # Simulation Direction NNN NNN -> Int
    # This function makes random silumation after taking a first step
    # in the given direction, then it returns the sum of scores obtained by all
    # the random moves
    def random_simulate_in_direction(self, dir, numberOfSteps, totalSims):

        board = self.board.copy_board()

        total_score = move_board(board,dir)
        if not game.movement.moved:
            return (total_score + settings.DEAD_BOARD_PENALTY)
        if game.movement.moved:
            board.generate_random_tile()

        for n in range(0,totalSims):

            tempboard = board.copy_board()

            for steps in range(1,numberOfSteps):
                total_score += move_board(tempboard,dir)
                if not board.check_board_moveable():
                    total_score += settings.DEAD_BOARD_PENALTY
                if game.movement.moved:
                    board.generate_random_tile()

        return total_score





