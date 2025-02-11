
from Games.ConnectFour import ConnectFour
from GameRunner import GameRunner
from Models.RandomModel import RandomModel

game = ConnectFour()
first = RandomModel()
second = RandomModel()
runner = GameRunner(game, first, second)
winner = runner.play()
