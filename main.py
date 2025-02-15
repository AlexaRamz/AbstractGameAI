
from Games.ConnectFour import ConnectFour
from GameRunner import GameRunner
from Models.MCTSModel import MCTSModel
from Models.HumanModel import HumanModel

game = ConnectFour()
first = MCTSModel()
second = HumanModel()
runner = GameRunner(game, first, second)
winner = runner.play(show=True)
