"""
play_nim.py - Play the Nim game with optional AI players.
Usage:
    python play_nim.py "<heaps>" <player1> <player2>
Example:
    python play_nim.py "[3, 4, 5]" ab random
"""
import sys, argparse
import games
import nim

# Define available player strategies
PLAYERS = {
    'me': games.query_player,
    'random': games.random_player,
    'alpha_beta': games.alpha_beta_player,
    'ab': games.alpha_beta_player,    # shorthand
}

def main():
    parser = argparse.ArgumentParser(description="Play Nim game with given heaps and players.")
    parser.add_argument("heaps", nargs="?", default="[3, 4, 5]",
                        help="Initial heaps as a list, e.g. \"[3,4,5]\"")
    parser.add_argument("player1", nargs="?", default="random",
                        help="Type of Player 1 (e.g. 'me', 'random', 'ab')")
    parser.add_argument("player2", nargs="?", default="random",
                        help="Type of Player 2 (e.g. 'me', 'random', 'ab')")
    args = parser.parse_args()

    # Parse the heaps argument which is given as a string representation of a list
    try:
        heaps = eval(args.heaps)
        if not (isinstance(heaps, list) and all(isinstance(x, int) and x >= 0 for x in heaps)):
            raise ValueError
    except:
        print("Error: 'heaps' argument must be a list of nonnegative integers, e.g., \"[3,4,5]\".")
        sys.exit(1)

    player1_type = args.player1
    player2_type = args.player2

    if player1_type not in PLAYERS or player2_type not in PLAYERS:
        print("Error: player type must be one of", list(PLAYERS.keys()))
        sys.exit(1)

    # Instantiate game
    game = nim.Nim(heaps=heaps)
    # Get the player functions
    player1_func = PLAYERS[player1_type]
    player2_func = PLAYERS[player2_type]

    print(f"Starting Nim game with heaps {heaps}. Player 1: {player1_type}, Player 2: {player2_type}")
    result_utility = game.play_game(player1_func, player2_func)
    # Interpret result utility:
    if result_utility == 1:
        print("Player 1 wins!")
    elif result_utility == -1:
        print("Player 2 wins!")
    else:
        print(f"Game ended with utility {result_utility} (draw or non-terminal state?)")

if __name__ == "__main__":
    main()
