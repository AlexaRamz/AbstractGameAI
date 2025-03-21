import random
from typing import Tuple, Optional

from Games.Game import Game, Player, Move
from Models.Model import Model

class Minimax(Model):

    MAX = +10000
    MIN = -10000

    def __init__(self, max_depth: int = 5):
        self.game = None
        self.player = None
        self.max_depth = max_depth

    def set_game_and_player(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def take_move(self):
        assert(self.game.get_current_player() == self.player)
        _, best_move = self.alphabeta(0, self.MIN, self.MAX, self.game.get_copy())
        self.game.perform_move(best_move)

    def alphabeta(self, depth, alpha, beta, game_state) -> Tuple[int, Optional[Move]]:
        if depth >= self.max_depth or game_state.is_game_over():
            return game_state.get_heuristic(), None
        current_player = game_state.get_current_player()
        moves = game_state.get_possible_moves()
        random.shuffle(moves)
        if current_player == Player.FIRST:
            value = self.MIN
            best_move = moves[0]
            for move in moves:
                game_state.perform_move(move)
                score, _ = self.alphabeta(depth + 1, alpha, beta, game_state)
                game_state.undo_move()
                if score > value:
                    value = score
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta: break
            return value, best_move
        else:
            value = self.MAX
            best_move = moves[0]
            for move in moves:
                game_state.perform_move(move)
                score, _ = self.alphabeta(depth + 1, alpha, beta, game_state)
                game_state.undo_move()
                if score < value:
                    value = score
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta: break
            return value, best_move