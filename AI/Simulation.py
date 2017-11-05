
from game.game_state import GameState
from game.movement import move_board
import game.movement
from AI import evaluation
import numpy as np
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
        print("median is : ", np.median(np.array(scores)))


    def evaluation_with_prediction_single_simulation(self):


        data = open("data.txt",'a')

        self.gs.reset()
        self.gs.board.generate_random_tile()

        data.write(self.gs.board.board_state_string())

        simFlag = self.gs.board.check_board_moveable()

        while simFlag:

            #self.gs.board.print_board()
            #print("score: ", self.gs.get_score(), "\n\n\n")


            moves_and_scores = evaluation.evaluate_and_predict_optmized_move(self.gs.board)

            score = "score: " + str(self.gs.get_score()) + "\n"
            data.write(score)
            data.write(str(moves_and_scores))
            data.write("\n\n")

            optimizedDir = evaluation.find_optimized_move(moves_and_scores)
            round_score = move_board(self.gs.board.get_board(), optimizedDir)

            self.gs.board.generate_random_tile()
            self.gs.add_score(round_score)

            data.write(self.gs.board.board_state_string())
            state_fitness = "State fitness: " + str(evaluation.evaluate_available_moves(self.gs.board.copy_board())) + "\n"
            data.write(state_fitness)


            if not self.gs.board.check_board_moveable():
                simFlag = False



        print("Simulation has ended, score is: ", self.gs.get_score())


        return self.gs.get_score()





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
        print("median is : ", np.median(np.array(scores)))





    #This function uses a evaluator function to find the optimized moving direction
    # It simulates by making the corresponding move.
    #
    def evaluation_single_simulation(self):

        self.gs.reset()
        self.gs.board.generate_random_tile()

        simFlag = True

        while simFlag:

            #self.gs.board.print_board()
            #print("score: ", self.gs.get_score(), "\n\n\n")


            moves_score = evaluation.evaluate_available_moves(self.gs.board.copy_board())
            print(moves_score)
            optimizedDir = evaluation.find_optimized_move(moves_score)
            round_score = move_board(self.gs.board.get_board(), optimizedDir)

            self.gs.board.generate_random_tile()
            self.gs.add_score(round_score)


            if not self.gs.board.check_board_moveable():
                simFlag = False


        self.gs.board.print_board()
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
        print("median is : ", np.median(np.array(scores)))





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
            round_score = move_board(self.gs.board.get_board(), optimizedDir)
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


        if board.check_board_moveable_in_dir(dir):
            total_score = move_board(board.get_board(),dir)
            board.generate_random_tile()

        else:
            return settings.DEAD_BOARD_PENALTY


        for n in range(0,totalSims):

            tempboard = board.copy_board()

            for steps in range(1,numberOfSteps):
                if board.check_board_moveable_in_dir(dir):
                    total_score += move_board(tempboard.get_board(), dir)
                    tempboard.generate_random_tile()
                else:
                    total_score += settings.DEAD_BOARD_PENALTY

        return total_score





if __name__ == "__main__":

    sim = Simulation()
    print("\n\n")

    bd = game.board.Board()

    board = np.array([[0, 0, 0, 2],
                      [0, 0, 0, 0],
                      [0, 0, 2, 0],
                      [0, 0, 8, 2]])

    for row in range(0,4):
        bd.set_row(row,board[row,:])

    sim.gs.board = bd

    sim.gs.board.print_board()


    moves_and_scores = sim.evaluate_and_predict_optmized_move()
    optimizedDir = evaluation.find_optimized_move(moves_and_scores)
    round_score = move_board(sim.gs.board.get_board(), optimizedDir)
    print("score:", moves_and_scores)

    print("\n\n")
    sim.gs.board.print_board()
    print(round_score)