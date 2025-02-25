
from typing import Any, Optional, List
from Games.Game import Game, Player, Move
import chess

class ChessMove(Move):

    def __init__(self, move: chess.Move):
        self.move = move

    def get_description(self) -> str:
        return self.move.uci()


class Chess(Game):

    def __init__(self, board: chess.Board = chess.Board()):
        self.board = board
        self.previous_move: Optional[ChessMove] = None

    def get_winner(self) -> Optional[Player]:
        if self.board.outcome() is None: return None
        winner = self.board.outcome().winner
        if winner == chess.WHITE: return Player.FIRST
        if winner == chess.BLACK: return Player.SECOND
        return None

    def get_possible_moves(self) -> List[ChessMove]:
        if self.board.outcome() is not None: return []
        return [ChessMove(move) for move in self.board.legal_moves]

    def get_description(self) -> str:
        return f"{self.board}"

    def get_opponent_move(self) -> Optional[Move]:
        return self.previous_move

    def get_current_player(self) -> Player:
        player = self.board.turn
        if player == chess.WHITE: return Player.FIRST
        if player == chess.BLACK: return Player.SECOND
        assert False

    def perform_move(self, move: ChessMove) -> None:
        self.previous_move = move
        self.board.push(move.move)

    def get_copy(self) -> Any:
        return Chess(self.board.copy())

    def get_neural_net_description_of_state(self) -> Any:
        # TODO: Implement
        pass