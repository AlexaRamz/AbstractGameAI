from Games.Chess import Chess
from Games.ConnectFour import ConnectFour
from GameRunner import GameRunner, GameRunnerComparisonResult
from Models.MCTS import MCTS
from Models.Minimax import Minimax
from Models.HumanModel import HumanModel
from Models.Model import Model
from Models.RandomModel import RandomModel
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def make_model(name: str) -> Model:
    if name == "random":
        return RandomModel()
    if name == "minimax":
        return Minimax()
    if name == "mcts":
        return MCTS()
    assert False

def run_connect_four(index, first: str, second: str) -> GameRunnerComparisonResult:
    connect_four = ConnectFour()
    res = GameRunner(connect_four, make_model(first), make_model(second)).compare_once()
    print(index, "connectfour", first, second, res.winner, res.average_first_player_turn_time, res.average_second_player_turn_time, res.total_time)
    return res

def run_connect_four_wrapper(args):
    return run_connect_four(*args)

if __name__ == '__main__':
    num_simulations = 100
    num_workers = mp.cpu_count()
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        seeds = [(i, "minimax", "mcts") for i in range(num_simulations)]
        result = list(executor.map(run_connect_four_wrapper, seeds))
    print(result)

