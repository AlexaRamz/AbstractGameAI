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

        input_str = input("Enter the move you would like to make (type '?' for list of possible moves): ")
        if input_str == "?":
            # List possible moves
            moves = self.game.get_possible_moves()
            for move in moves:
                print(move.get_description())
            self.take_move()
            return

        success = self.game.perform_move_from_str(input_str)
        if success == False:
            print("Input was invalid or move could not be made. Try again.")
            self.take_move()
