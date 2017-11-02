
from game.game_state import GameState
from game.movement import move_board
import game.movement
from AI.evaluation import board_evaluator_in_dir, evaluate_available_moves, find_optimized_move, evaluate_board_state

import settings


class Simulation:

    def __init__(self):

        self.gs = GameState()
        self.gs.board.generate_random_tile()




    # This simulator is similar to evaluation simulator
    # however, it implements prediction moves so that the movement won't
    # focus on maximizing scores for each move; instead, the ai also considers
    # how each move will affect the board in the preceding rounds.
    def evaluation_with_prediction_simulator(self,rounds = 1):

        rounds = rounds

        scores = []

        while rounds > 0:

            print("round: ", rounds)
            score = self.evaluation_with_prediction_single_simulation()
            scores.append(score)
            rounds -= 1

        print("scores for the rounds simulated are: ", scores)


    def evaluation_with_prediction_single_simulation(self):

        self.gs.reset()
        self.gs.board.generate_random_tile()

        simFlag = True

        while simFlag:

            self.gs.board.print_board()
            print("score: ", self.gs.get_score(), "\n\n\n")


            moves_and_scores = self.evaluate_and_predict_optmized_move()
            optimizedDir = find_optimized_move(moves_and_scores)
            round_score = move_board(self.gs.board, optimizedDir)

            self.gs.board.generate_random_tile()
            self.gs.add_score(round_score)


            if not self.gs.board.check_board_moveable():
                simFlag = False



        print("Simulation has ended")

        return self.gs.get_score()

    def evaluate_and_predict_optmized_move(self):

        scores = {settings.Direction.up: 0, settings.Direction.right: 0, settings.Direction.left: 0,
                  settings.Direction.down: 0}

        for dir in settings.Direction:
            move_board(self.gs.board.copy_board(),dir)
            if not game.movement.moved:
                  scores.pop(dir)
            else:
                copy_board = self.gs.board.copy_board()
                move_score = move_board(copy_board,dir)
                board_state_score = evaluate_board_state(copy_board)
                scores[dir] = move_score + board_state_score

        return scores



    #
    # This simulator uses evaluation_simulation to make optimized move, and simulates the game
    def evaluation_simulator(self,rounds = 1):

        rounds = rounds

        scores = []

        while rounds > 0:

            print("round: ", rounds)
            score = self.evaluation_single_simulation()
            scores.append(score)
            rounds -= 1

        print("scores for the rounds simulated are: ", scores)





    #This function uses a evaluator function to find the optimized moving direction
    # It simulates by making the corresponding move.
    #
    def evaluation_single_simulation(self):

        self.gs.reset()
        self.gs.board.generate_random_tile()

        simFlag = True

        while simFlag:

            self.gs.board.print_board()
            print("score: ", self.gs.get_score(), "\n\n\n")


            moves_score = evaluate_available_moves(self.gs.board.copy_board())
            optimizedDir = find_optimized_move(moves_score)
            round_score = move_board(self.gs.board, optimizedDir)

            self.gs.board.generate_random_tile()
            self.gs.add_score(round_score)


            if not self.gs.board.check_board_moveable():
                simFlag = False


        print("Simulation has ended")

        return self.gs.get_score()






    # NNN NNN NNN -> Void
    # Rounds represent the number of simulations desired
    # num_of_steps represents the number of steps wanted into each direction
    # sim_in_dir represents the number of random movements wanted after going into one direction

    # A single simulation breaks when:
    #

    def random_simulator(self,rounds = 1, num_of_steps = settings.DEFAULT_NUMBER_OF_STEPS, sim_in_dir = settings.DEFAULT_SIMULATIONS_IN_EACH_DIRECTION):

        rounds = rounds

        scores = []

        while rounds > 0:

            print("round: ", rounds)
            score = self.random_single_simulation(num_of_steps,sim_in_dir)
            scores.append(score)
            rounds -= 1

        print("scores for the rounds simulated are: ", scores)





    # This Function simulates a single simulation
    # It starts with resetting and ends when the board is not moveable in any direction
    def random_single_simulation(self, num_of_steps, sim_in_dir):

        self.gs.reset()

        self.gs.board.generate_random_tile()
        Simflag = True

        while Simflag:

            self.gs.board.print_board()
            print("score: ", self.gs.get_score(), "\n\n\n")

            optimizedDir = self.random_simulate(num_of_steps, sim_in_dir)
            round_score = move_board(self.gs.board, optimizedDir)
            self.gs.board.generate_random_tile()
            self.gs.add_score(round_score)

            if not self.gs.board.check_board_moveable():
                Simflag = False
                self.gs.board.generate_random_tile()

        print("simulation ended.")

        return self.gs.get_score()





    # Simulation  -> Direction
    # This Function finds the optimized move by first moving in each direction
    # Then it randomly generates moves from that point, based on
    #   - num_of_steps
    #   - sims_in_each_dir
    # It returns the direction that yields the best average score
    def random_simulate(self, num_of_steps, sim_in_dir):

        scores = {settings.Direction.up: 0, settings.Direction.right: 0, settings.Direction.left: 0, settings.Direction.down: 0}

        for dir in settings.Direction:

            scores[dir] += self.random_simulate_in_direction(dir, num_of_steps, sim_in_dir)

        max_dir = settings.Direction.up

        for dir in settings.Direction:
            if scores[dir] > scores[max_dir]:
                max_dir = dir
            print(dir, scores[dir])


        return max_dir


    # Simulation Direction NNN NNN -> Int
    # This function makes random silumation after taking a first step
    # in the given direction, then it returns the sum of scores obtained by all
    # the random moves
    def random_simulate_in_direction(self, dir, numberOfSteps, totalSims):

        board = self.gs.board.copy_board()

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





