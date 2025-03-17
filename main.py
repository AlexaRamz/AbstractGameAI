from Games.Chess import Chess
from Games.ConnectFour import ConnectFour
from GameRunner import GameRunner, GameRunnerComparisonResult
from Models.MCTSModel import MCTSModel
from Models.MinimaxABModel import MinimaxABModel
from Models.HumanModel import HumanModel
from Models.Model import Model
from Models.RandomModel import RandomModel
import multiprocessing as mp
import chess
import os
from concurrent.futures import ProcessPoolExecutor

def make_model(name: str) -> Model:
    if name == "random":
        return RandomModel()
    if name == "minimax":
        return MinimaxABModel()
    assert False

def run_chess(index, first: str, second: str) -> GameRunnerComparisonResult:
    chess = Chess()
    res = GameRunner(chess, make_model(first), make_model(second)).compare_once()
    print("Chess", first, second, res.winner, res.average_first_player_turn_time, res.average_second_player_turn_time, res.total_time)
    return res

num_simulations = 100
num_workers = mp.cpu_count()

def run_chess_wrapper(args):
    return run_chess(*args)

if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        seeds = [(i, "minimax", "random") for i in range(num_simulations)]
        result = list(executor.map(run_chess_wrapper, seeds))
    print(result)

