"""
nim.py - Starter code for Nim game implementation.
"""
from games import Game, GameState

class Nim(Game):
    def __init__(self, heaps=[3, 4, 5]):
        """Initialize the Nim game with given heap sizes."""
        # Initialize the game state (to_move and heaps)
        # 'to_move' should be 'Player 1' initially.
        # 'heaps' can be stored as a tuple or list of heap counts.
        self.initial = GameState(to_move='Player 1', utility=0, board=tuple(heaps), moves=None)

    def actions(self, state):
        """Return a list of the allowable moves (heap_index, number_removed) at this point."""
        moves = []
        # TODO: Generate all valid moves. For each heap that has at least 1 object,
        # generate moves for removing 1 up to all objects in that heap.
        i = 0
        for heap in state.board:
            for j in range(heap):
                moves.append((i, (j + 1)))
            i += 1
        return moves

    def result(self, state, move):
        """Return the state that results from making a move from the given state."""
        # TODO: Apply the move to the state to get the new state.
        # - move is a tuple (heap_index, number_removed)
        # - subtract number_removed from the specified heap
        # - switch the player turn
        i, x = move
        heaps = list(state.board)
        player = state.to_move
        new_util = state.utility

        heaps[i] -= x
        new_state = GameState(to_move=('Player 2' if player == 'Player 1' else 'Player 1'), utility=new_util, board=heaps, moves=state.moves)

        if(self.terminal_test(new_state)):
            if player == 'Player 1':
                new_util = 1
            else:
                new_util = -1

        return GameState(to_move=('Player 2' if player == 'Player 1' else 'Player 1'), utility=new_util, board=heaps, moves=state.moves)

    def terminal_test(self, state):
        """Return True if the state is a terminal state (no moves left)."""
        # TODO: Check if all heaps are empty.

        for heap in state.board:
            if heap > 0:
                return False

        return True

    def utility(self, state, player):
        """Return the value of this final state to the given player."""
        # TODO: Compute the utility of the terminal state.
        # Return the utility from the perspective of the player
        # - If player is 'Player 1' and they win, return self.utility
        # - If player is 'Player 2' and they win, return -self.utility
        # See TicTacToe for an example.
        return state.utility if player == 'Player 1' else -state.utility

    def display(self, state):
        """Print or display the state in a human-readable format."""
        # TODO: Print the state (whose turn and heap sizes).
        print(f"{state}")  # Simple default: print the state object (you can improve this)
