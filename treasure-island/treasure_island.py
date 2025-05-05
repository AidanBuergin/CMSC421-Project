# treasure_island_solution.py

from mdp import MDP, GridMDP
from utils import vector_add, orientations

class TreasureIslandMDP(GridMDP):
    """Solution implementation of the Treasure Island MDP."""
    def __init__(self, grid_map, reward_func, init=(0, 0), gamma=0.9):
        #### Implementation here ####
        reward = []
        terminals = []

        for y, str in enumerate(grid_map):
            r_row = []
            for x, c in enumerate(str):
                if c == 'X':
                    r_row.append(None)
                else:
                    if c == 'O' or c == 'T':
                        print('terminal')
                        terminals.append((x,((len(grid_map)-1) - y)))
                    print(y, x)
                    r_row.append(reward_func(x, y))
            reward.append(r_row)

        # It's easiest to call the based GridMDP class with the right set of inputs
        super().__init__(reward, terminals, init, gamma)
