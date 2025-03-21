from abc import ABC, abstractmethod
from Games.Game import Game, Player

class Model(ABC):

    @abstractmethod
    def set_game_and_player(self, game: Game, player: Player):
        # Sets up the model to play the given game as the given player
        pass

    @abstractmethod
    def take_move(self):
        # Makes a move on the game
        # This should only be called when game's current player is this model
        pass