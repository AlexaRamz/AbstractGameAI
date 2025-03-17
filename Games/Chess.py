
from typing import Any, Optional, List
from Games.Game import Game, Player, Move
import chess

class ChessMove(Move):

    def __init__(self, move: chess.Move):
        self.move = move

    def get_description(self) -> str:
        return self.move.uci()

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

class Chess(Game):

    def __init__(self, board: chess.Board = None):
        self.board = board if board is not None else chess.Board()

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
        return f"{self.board}\n"

    def get_opponent_move(self) -> Optional[Move]:
        if len(self.board.move_stack) == 0: return None
        return ChessMove(self.board.peek())

    def get_current_player(self) -> Player:
        player = self.board.turn
        if player == chess.WHITE: return Player.FIRST
        if player == chess.BLACK: return Player.SECOND
        assert False

    def perform_move(self, move: ChessMove) -> None:
        self.board.push(move.move)

    def get_copy(self) -> Any:
        return Chess(self.board.copy())

    def get_neural_net_description_of_state(self) -> Any:
        # TODO: Implement
        pass

    def is_game_over(self) -> bool:
        return self.board.outcome() is not None

    def score_position(self, player: Player) -> int:
        score = 0
        for piece_type, value in PIECE_VALUES.items():
            score += len(self.board.pieces(piece_type, chess.WHITE)) * value
            score -= len(self.board.pieces(piece_type, chess.BLACK)) * value
        if player == Player.SECOND:
            score *= -1
        return score

    def perform_move_from_str(self, move: str) -> bool:
        try:
            move = chess.Move.from_uci(move)
            self.perform_move(ChessMove(move))
            return True
        except ValueError:
            return False

    def undo_move(self) -> None:
        self.board.pop()
