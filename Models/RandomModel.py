import random

from Games.Game import Game, Player
from Models.Model import Model

class RandomModel(Model):

    def __init__(self):
        self.game = None
        self.player = None

    def set_game_and_player(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def take_move(self):
        assert(self.game.get_current_player() == self.player)
        moves = self.game.get_possible_moves()
        selected_move = random.choice(moves)
        self.game.perform_move(selected_move)