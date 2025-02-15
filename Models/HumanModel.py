from Games.Game import Game, Player
from Models.Model import Model
from typing import Optional

# This is a model that allows a human to play any of the games
# The human says the index of a move they would like to play
class HumanModel(Model):

    def __init__(self):
        self.game = None
        self.player = None

    def set_game_and_player(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def take_move(self):
        assert(self.game.get_current_player() == self.player)
        moves = self.game.get_possible_moves()
        for index in range(len(moves)):
            print(str(index) + " " + moves[index].get_description())
        index = self.read_input(len(moves))
        move = moves[index]
        self.game.perform_move(move)

    def read_input(self, count) -> int:
        index = self.read_int()
        while index is None or index < 0 or index >= count:
            print("Invalid index, try again.")
            index = self.read_int()
        return index

    def read_int(self) -> Optional[int]:
        response = input("Enter the index of the move you would like to make.")
        try:
            value = int(response)
        except ValueError:
            value = None
        return value