# treasure_island_solution.py

from mdp import MDP, GridMDP
from utils import vector_add, orientations

class TreasureIslandMDP(GridMDP):
    """Solution implementation of the Treasure Island MDP."""
    def __init__(self, grid_map, reward_func, init=(0, 0), gamma=0.9):
        #### Implementation here ####

        # It's easiest to call the based GridMDP class with the right set of inputs
        super().__init__(reward, terminals, init, gamma)
