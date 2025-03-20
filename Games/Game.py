
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, TypeVar, List, Optional

# A Player is either first or second
# This is used to report the winner and keep track of the current player
class Player(Enum):
    FIRST = 0
    SECOND = 1

# Each game can have a different Move type
class Move(ABC):

    @abstractmethod
    def get_description(self) -> str:
        # A string describing the move
        pass

# A Game defines a unified API for all games that we will be testing
class Game(ABC):

    @abstractmethod
    def get_winner(self) -> Optional[Player]:
        # returns the winner of the game
        # None if the game is not over or has ended in a tie
        pass

    @abstractmethod
    def is_game_over(self) -> bool:
        # returns whether the game is over (no moves possible for either player)
        pass

    @abstractmethod
    def score_position(self, player: Player) -> int:
        # returns an evaluation of the board positions for this player
        pass

    def get_heuristic(self) -> int:
        # positive means good for the FIRST player, negative means good for the SECOND player
        if self.is_game_over():
            winner = self.get_winner()
            if winner == Player.FIRST:
                return +10000
            elif winner == Player.SECOND:
                return -10000
            else:
                return 0
        else:
            return self.score_position(Player.FIRST)
    
    def get_value_and_terminated(self) -> int|bool:
        if self.is_game_over():
            winner = self.get_winner()
            value = 0
            if winner == Player.FIRST:
                value = +10000
            elif winner == Player.SECOND:
                value =  -10000
            return value, True
        else:
            return self.score_position(self.get_current_player()), False

    @abstractmethod
    def get_possible_moves(self) -> List[Move]:
        # returns a list of all possible moves for the current player
        # empty if game is over
        pass

    @abstractmethod
    def get_description(self) -> str:
        # returns the string representation of the game state
        pass

    @abstractmethod
    def get_opponent_move(self) -> Optional[Move]:
        # returns the move the opponent made, if any
        pass

    @abstractmethod
    def get_current_player(self) -> Player:
        # returns the current player (either first or second)
        pass

    @abstractmethod
    def perform_move(self, move: Move) -> None:
        # performs a move and switches to the other players turn
        # to construct a move, call get_possible_moves
        pass

    @abstractmethod
    def undo_move(self) -> None:
        # Undoes the most recent move
        # This may you can explore a hypothetical without copying
        pass

    @abstractmethod
    def perform_move_from_str(self, move: Move) -> bool:
        # performs a move from an input string
        # returns true if the string is valid and the move was successful
        pass

    @abstractmethod
    def get_copy(self) -> "Game":
        # returns a copy of self
        # this is useful for trying out moves without affecting the original
        pass

    @abstractmethod
    def get_neural_net_description_of_state(self) -> Any:
        # returns a description of the current state in a format ready for the NN
        # TODO: Figure out what type to return from this
        pass

    @abstractmethod
    def get_board_info(self) -> int | int | List[Any]:
        # returns the width and height of the game board, and the list of all pieces that can be placed on a board space (including empty)
        pass

    @abstractmethod
    def get_board(self):
        """Returns the game board as a 2D numpy array"""
        pass
