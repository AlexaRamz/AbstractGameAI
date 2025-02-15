
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
        # None if the game is not over
        pass

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
    def get_copy(self) -> Any:
        # returns a copy of self
        # this is useful for trying out moves without affecting the original
        pass

    @abstractmethod
    def get_neural_net_description_of_state(self) -> Any:
        # returns a description of the current state in a format ready for the NN
        # TODO: Figure out what type to return from this
        pass