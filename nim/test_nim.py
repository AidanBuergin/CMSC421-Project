# nim_unittest.py
import unittest
from nim import Nim
from games import alpha_beta_player
from games import Game

class TestNimGame(unittest.TestCase):
    def setUp(self):
        """Initialize a game for testing."""
        self.game = Nim()  # default heaps [3,4,5]
    
    def test_actions_initial(self):
        """Initial state should have 12 possible moves (3+4+5)."""
        state = self.game.initial
        moves = self.game.actions(state)
        self.assertIsInstance(moves, list, "actions() should return a list")
        # There should be 12 moves in any order
        self.assertEqual(len(moves), 12, "Initial state should have 12 moves (3+4+5).")
        # Check that moves cover all possible removals
        expected_moves = {(0,1),(0,2),(0,3),
                          (1,1),(1,2),(1,3),(1,4),
                          (2,1),(2,2),(2,3),(2,4),(2,5)}
        self.assertEqual(set(moves), expected_moves, "actions() did not return the correct set of moves.")
    
    def test_result_basic(self):
        """Applying a move should return a new state with updated heaps and toggled player."""
        state = self.game.initial  # [3,4,5], Player 1 to move
        move = (1, 2)  # remove 2 from heap index 1 (the heap of 4 -> will become 2)
        new_state = self.game.result(state, move)
        # Heaps should reflect the move
        self.assertEqual(list(new_state.board), [3, 2, 5], "Heap sizes not updated correctly after move.")
        # Player should switch from Player 1 to Player 2
        self.assertEqual(new_state.to_move, 'Player 2', "Player turn did not switch after the move.")
        # Utility should remain 0 (not terminal yet)
        self.assertEqual(new_state.utility, 0, "Utility should be 0 for non-terminal state.")
        # Original state should remain unchanged (immutability)
        self.assertEqual(list(state.board), [3, 4, 5], "Original state should not be modified by result().")
    
    def test_result_terminal(self):
        """Applying a move that takes the last object should result in a terminal state with correct utility."""
        # Create a state where one move will finish the game.
        # For example, heap sizes [0, 1, 0] and it's Player 1's turn. Player 1 can take the 1 from heap1 and win.
        custom_game = Nim(heaps=[0, 1, 0])
        state = custom_game.initial
        self.assertTrue(custom_game.actions(state) == [(1,1)], "Only one move should be available to take the last object.")
        final_state = custom_game.result(state, (1, 1))
        # Now all heaps should be 0 (terminal)
        self.assertTrue(custom_game.terminal_test(final_state), "State should be terminal after taking last object.")
        # The move was made by Player 1, so Player 1 should be the winner -> utility = 1 for Player 1
        self.assertEqual(final_state.utility, 1, "Utility should be +1 when Player 1 wins.")
        # For Player 2, utility should be -1
        self.assertEqual(custom_game.utility(final_state, 'Player 2'), -1, "Utility should be -1 when Player 1 wins.")
        # Next player in final state would be Player 2 (though game is over, it's Player 2's 'turn' with no moves)
        self.assertEqual(final_state.to_move, 'Player 2', "After Player 1 takes last object, to_move should be Player 2 (no moves for Player 2).")
    
    def test_multiple_moves_sequence(self):
        """Simulate a sequence of moves to ensure state progression is correct."""
        # Player 1: remove 3 from heap2 (5->2)
        s1 = self.game.result(self.game.initial, (2, 3))
        self.assertEqual(list(s1.board), [3, 4, 2])
        self.assertEqual(s1.to_move, 'Player 2')
        self.assertFalse(self.game.terminal_test(s1))
        # Player 2: remove 1 from heap0 (3->2)
        s2 = self.game.result(s1, (0, 1))
        self.assertEqual(list(s2.board), [2, 4, 2])
        self.assertEqual(s2.to_move, 'Player 1')
        self.assertFalse(self.game.terminal_test(s2))
        # Player 1: remove 2 from heap0 (2->0)
        s3 = self.game.result(s2, (0, 2))
        self.assertEqual(list(s3.board), [0, 4, 2])
        self.assertEqual(s3.to_move, 'Player 2')
        self.assertFalse(self.game.terminal_test(s3))
        # Player 2: remove 2 from heap2 (2->0)
        s4 = self.game.result(s3, (2, 2))
        self.assertEqual(list(s4.board), [0, 4, 0])
        self.assertEqual(s4.to_move, 'Player 1')
        self.assertFalse(self.game.terminal_test(s4))
        # Player 1: remove all 4 from heap1 (4->0), this ends the game
        s5 = self.game.result(s4, (1, 4))
        self.assertEqual(list(s5.board), [0, 0, 0])
        self.assertTrue(self.game.terminal_test(s5))
        # Player 1 made the last move, so Player 1 wins
        self.assertEqual(s5.utility, 1)
        self.assertEqual(s5.to_move, 'Player 2')  # It would be O's turn, but no moves remain.

    def test_gameplay(self):
        """Simulate a bunch of games using AI vs AI to ensure gameplay works correctly."""
        # Simulate 
        game = Nim(heaps=[3, 4, 5])
        utility = game.play_game(alpha_beta_player, alpha_beta_player)  # Play the game!
        # Ensure the utility is either 1 (Player 1 wins) or -1 (Player 2 wins)
        self.assertEqual(utility, 1, "Utility should be 1 (Player 1 wins).")

        game = Nim(heaps=[0, 1, 1])
        utility = game.play_game(alpha_beta_player, alpha_beta_player)  # Play the game!
        # Ensure the utility is either 1 (Player 1 wins) or -1 (Player 2 wins)
        self.assertEqual(utility, -1, "Utility should be -1 (Player 2 wins).")

        game = Nim(heaps=[0, 2, 0])
        utility = game.play_game(alpha_beta_player, alpha_beta_player)  # Play the game!
        # Ensure the utility is either 1 (Player 1 wins) or -1 (Player 2 wins)
        self.assertEqual(utility, 1, "Utility should be 1 (Player 1 wins).")

        game = Nim(heaps=[2, 3, 1])
        utility = game.play_game(alpha_beta_player, alpha_beta_player)  # Play the game!
        # Ensure the utility is either 1 (Player 1 wins) or -1 (Player 2 wins)
        self.assertEqual(utility, -1, "Utility should be -1 (Player 2 wins).")
    
    def test_nim_subclass(self):
        # Ensure Nim is a subclass of Game
        self.assertTrue(issubclass(Nim, Game))
        # And that the game object is instance of Game
        self.assertIsInstance(self.game, Game)

if __name__ == "__main__":
    unittest.main(verbosity=2)
