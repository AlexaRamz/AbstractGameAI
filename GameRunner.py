
from Games.Game import Game, Player
from Models.Model import Model

class GameRunner:

    def __init__(self, game: Game, player_one: Model, player_two: Model):
        # Creates a GameRunner where the two models play the given game
        self.game = game
        self.player_one = player_one
        self.player_two = player_two
        self.player_one.set_game_and_player(game, Player.FIRST)
        self.player_two.set_game_and_player(game, Player.SECOND)

    def play(self, show = False) -> Player:
        # Play as many turns of the game as are required to determine a winner
        # The winning player is returned
        if show: print(self.game.get_description())
        while self.game.get_winner() is None:
            current = self.game.get_current_player()
            if current == Player.FIRST:
                self.player_one.take_move()
            else:
                self.player_two.take_move()
            if show: print(self.game.get_description())
        return self.game.get_winner()