# play_treasure_island.py

from mdp import *
from reinforcement_learning import QLearningAgent, run_single_trial
from treasure_island import TreasureIslandMDP
from utils import *

# Define a reward function for the MDP.
# The function now takes the grid as an additional parameter.
def reward_function(x, y, grid):
    # Example: +10 for treasure, -0.1 for each step on normal ground.
    if grid[y][x] == 'T':  # Assuming 'T' represents treasure in the grid
        return +1
    elif grid[y][x] == 'O':  # Assuming 'O' represents obstacles
        return -1.0  # Penalty for obstacles (if needed)
    else:
        return -0.04  # Default penalty for normal ground

# Define the map 
default_map = [
    ".O..T",
    ".X..O",
    "....."
]

# Instantiate the MDP with the map and reward function
mdp = TreasureIslandMDP(default_map, lambda x, y: reward_function(x, y, default_map), init=(0, 0), gamma=0.9)

# Set up a Q-learning agent with an epsilon-greedy strategy. Parameters:
# - mdp: the MDP environment
# - alpha: learning rate function (optional)
# Set Rplus to be greater than your greatest reward. 
# You can play around with the others but the default should be reasonable.
agent = QLearningAgent(mdp, Ne=5, Rplus=200, alpha=lambda n: 60./(59+n))

# Run multiple episodes of learning
num_episodes = 1000
print("Running Q-learning for {} episodes...".format(num_episodes))
treasure_count = 0
for episode in range(num_episodes):
    run_single_trial(agent, mdp)

# print("Learned Q-values:")
# print(agent.Q)

# After learning, let's extract the learned policy.
learned_policy = {}
for s in mdp.states:
    if s in mdp.terminals:
        learned_policy[s] = None
    else:
        possible_actions = mdp.actions(s)
        if not possible_actions:
            learned_policy[s] = None
        else:
            best_a = max(possible_actions, key=lambda a: agent.Q[(s, a)])
            learned_policy[s] = best_a

# Display the policy in a readable format (arrows for directions, . for terminal).
policy_grid = mdp.to_arrows(learned_policy)
print("Learned Policy (arrows show direction):")
print_table(policy_grid)