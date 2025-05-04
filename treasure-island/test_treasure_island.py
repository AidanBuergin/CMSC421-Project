
import unittest
from treasure_island import TreasureIslandMDP

def simple_reward(x, y):
    return 0.0

class TreasureIslandMDPTests(unittest.TestCase):
    def setUp(self):
        self.map3 = [
            "..T",
            ".O.",
            ".X."
        ]
        self.mdp3 = TreasureIslandMDP(self.map3, simple_reward, init=(0,0), gamma=0.9)

    def test_state_space(self):
        # States should not include walls (X)
        self.assertNotIn((1,0), self.mdp3.states)

    def test_terminal_states(self):
        # Obstacles (O) and Treasures (T) should be terminals
        self.assertIn((1,1), self.mdp3.terminals)  # Obstacle
        self.assertIn((2,2), self.mdp3.terminals)  # Treasure

    def test_non_terminal_states(self):
        # Normal cells should not be terminals
        self.assertNotIn((0,0), self.mdp3.terminals)
        self.assertNotIn((0,1), self.mdp3.terminals)

    def test_transition_probabilities_sum(self):
        for state in self.mdp3.states:
            if state in self.mdp3.terminals:
                continue
            for action in self.mdp3.actlist:
                outcomes = self.mdp3.T(state, action)
                total_prob = sum(prob for prob, _ in outcomes)
                self.assertTrue(abs(total_prob - 1.0) < 1e-6)

if __name__ == "__main__":
    unittest.main()
