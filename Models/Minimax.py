import random
from Games.Game import Game, Player, Move
from Models.Model import Model
from typing import Tuple, Optional

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
        _, best_move = self.alphabeta(0, self.MIN, self.MAX)
        self.game.perform_move(best_move)

    def alphabeta(self, depth, alpha, beta) -> Tuple[int, Optional[Move]]:
        if depth >= self.max_depth or self.game.is_game_over():
            return self.game.get_heuristic(), None
        current_player = self.game.get_current_player()
        moves = self.game.get_possible_moves()
        random.shuffle(moves)
        if current_player == Player.FIRST:
            value = self.MIN
            best_move = moves[0]
            for move in moves:
                self.game.perform_move(move)
                score, _ = self.alphabeta(depth + 1, alpha, beta)
                self.game.undo_move()
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
                self.game.perform_move(move)
                score, _ = self.alphabeta(depth + 1, alpha, beta)
                self.game.undo_move()
                if score < value:
                    value = score
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta: break
            return value, best_move