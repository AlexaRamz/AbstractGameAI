from typing import Tuple, Optional
from Games.Game import Game, Player
from Models.Model import Model
import time

class GameRunnerComparisonResult:
    def __init__(self, winner: Optional[Player], average_first_player_turn_time: float, average_second_player_turn_time: float, total_time: float):
        self.winner = winner
        self.average_first_player_turn_time = average_first_player_turn_time
        self.average_second_player_turn_time = average_second_player_turn_time
        self.total_time = total_time

class GameRunner:

    def __init__(self, game: Game, player_one: Model, player_two: Model):
        # Creates a GameRunner where the two models play the given game
        self.game = game
        self.player_one = player_one
        self.player_two = player_two
        self.player_one.set_game_and_player(game, Player.FIRST)
        self.player_two.set_game_and_player(game, Player.SECOND)
        self.active = True

    def play(self, show = False) -> Player:
        assert self.active
        self.active = False
        # Play as many turns of the game as are required to determine a winner
        # The winning player is returned
        if show: print(self.game.get_description())
        while not self.game.is_game_over():
            current = self.game.get_current_player()
            if current == Player.FIRST:
                self.player_one.take_move()
            else:
                self.player_two.take_move()
            if show: print(self.game.get_description())
        return self.game.get_winner()

    def compare_once(self) -> GameRunnerComparisonResult:
        assert self.active
        self.active = False

        # Stats:
        num_first_player_turns = 0
        total_first_player_turn_time = 0.0
        num_second_player_turns = 0
        total_second_player_turn_time = 0.0

        assert self.game.get_opponent_move() is None
        assert not self.game.is_game_over()

        game_start = time.time()

        while not self.game.is_game_over():
            current = self.game.get_current_player()
            if current == Player.FIRST:
                start = time.time()
                self.player_one.take_move()
                end = time.time()
                num_first_player_turns += 1
                total_first_player_turn_time += (end - start)
            else:
                start = time.time()
                self.player_two.take_move()
                end = time.time()
                num_second_player_turns += 1
                total_second_player_turn_time += (end - start)
        winner = self.game.get_winner()

        game_end = time.time()

        assert num_first_player_turns > 0 and num_second_player_turns > 0

        return GameRunnerComparisonResult(
            winner,
            total_first_player_turn_time / num_first_player_turns,
            total_second_player_turn_time / num_second_player_turns,
            game_end - game_start
        )
