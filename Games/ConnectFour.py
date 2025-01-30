from typing import Any, Self, List
from Games.Game import Game, Player

class ConnectFourMove:
    def __init__(self, column: int):
        self.column = column

class ConnectFour(Game):

    def __init__(self):
        # TODO: Implement
        pass

    def get_winner(self) -> Player | None:
        # TODO: Implement
        pass

    def get_possible_moves(self) -> List[ConnectFourMove]:
        # TODO: Implement
        pass

    def get_current_player(self) -> Player:
        # TODO: Implement
        pass

    def perform_move(self, move: ConnectFourMove) -> None:
        # TODO: Implement
        pass

    def get_copy(self) -> Self:
        # TODO: Implement
        pass

    def get_neural_net_description_of_state(self) -> Any:
        # TODO: Implement
        pass