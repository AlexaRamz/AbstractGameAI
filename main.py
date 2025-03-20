import argparse

from Games.Game import Player
from Games.ConnectFour import ConnectFour
from Games.Chess import Chess
from GameRunner import GameRunner, GameRunnerComparisonResult

from Models.Model import Model
from Models.HumanModel import HumanModel
from Models.Minimax import Minimax
from Models.MCTS import MCTS
from Models.AlphaZero.AlphaZeroModel import AlphaZeroModel
from Models.AlphaZero.AlphaZeroConfig import connectfour_config
from Models.RandomModel import RandomModel

def make_model(name: str) -> Model:
    """Returns the specified model."""
    if name == "human":
        return HumanModel()
    if name == "random":
        return RandomModel()
    if name == "minimax":
        return Minimax()
    if name == "mcts":
        return MCTS()
    if name == "alphazero":
        return AlphaZeroModel(connectfour_config)

def run_game(game, player1, player2):
    """Runs the specified game with the specified players."""
    if game == "chess" and player2 == "alphazero":
      print("AlphaZero is not yet implemented for chess")
      return
    
    print(f"Running {game} with {player1} vs {player2}")
    
    if game == "connect4":
        game_instance = ConnectFour()
    elif game == "chess":
        game_instance = Chess()

    winner = GameRunner(game_instance, make_model(player1), make_model(player2)).play(show=True)
    if winner == Player.FIRST:
        print(f"{player1} wins!")
    elif winner == Player.SECOND:
        print(f"{player2} wins!")
    else:
        print("Draw!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a game with specified players.")
    parser.add_argument("game", choices=["connect4", "chess"], help="The game to play.")
    parser.add_argument("player1", choices=["human", "minimax", "mcts", "alphazero", "random"], help="Player 1 type.")
    parser.add_argument("player2", choices=["human", "minimax", "mcts", "alphazero", "random"], help="Player 2 type.")

    args = parser.parse_args()

    run_game(args.game, args.player1, args.player2)