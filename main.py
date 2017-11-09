
from game.game_runner import GameRunner

from AI.Simulation import Simulation

import settings




#runner = GameRunner()
#rrunner.run()


sim = Simulation()

#settings.TILE_WEIGHT_MATRIX = settings.TILE_WEIGHT_MATRIX1

#sim.alphabeta_evaluation_sim(3,30)

settings.TILE_WEIGHT_MATRIX = settings.TILE_WEIGHT_MATRIX2

sim.alphabeta_evaluation_sim(3,30)

#settings.TILE_WEIGHT_MATRIX = settings.TILE_WEIGHT_MATRIX3

#sim.alphabeta_evaluation_sim(3,30)


