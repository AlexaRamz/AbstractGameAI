from typing import Any, List, Optional
from Games.Game import Game, Player, Move
import copy

class ConnectFourMove(Move):
    def __init__(self, column: int):
        self.column = column

    def get_description(self) -> str:
        return str(self.column)

    def __eq__(self, other):
        return isinstance(other, ConnectFourMove) and self.column == other.column

    def __hash__(self):
        return hash(self.column)

    def __repr__(self):
        return f"ConnectFourMove({self.column})"

class ConnectFour(Game):
    
    def __init__(self):
        self.previous_move = None
        self.NUM_ROWS, self.NUM_COLUMNS = (6, 7)
        self.board = [[-1 for i in range(self.NUM_COLUMNS)] for j in range(self.NUM_ROWS)]
        self.current_player = Player.FIRST
        self.movesMade = 0

    def get_row_winner(self, row: int) -> int:
        color = -1
        count = 0

        for slot in self.board[row]:
            if slot != color:
                color = slot
                count = 1
            elif slot == color and slot != -1:
                count += 1
            if count == 4:
                return color
        return -1
    
    def get_column_winner(self, col: int) -> int:
        color = -1
        count = 0

        for row in range(self.NUM_ROWS - 1, -1, -1):
            slot = self.board[row][col]
            if slot != color:
                color = slot
                count = 1
            elif slot == color and slot != -1:
                count += 1
            if count == 4:
                return color
        return -1
    
    def get_diagonal_winner(self, row_start: int, column_start: int, mainDiagonal: bool):
        row = row_start
        col = column_start

        color = -1
        count = 0

        while row >= 0 and row < self.NUM_ROWS and col >= 0 and col < self.NUM_COLUMNS:
            slot = self.board[row][col]

            if slot != color:
                color = slot
                count = 1
            elif slot == color and slot != -1:
                count += 1
            
            if count == 4:
                return color
            
            if mainDiagonal:
                row += 1
            else:
                row -= 1
            col += 1
        return -1

    def game_over(self):    
        # Check if no more moves can be made
        if self.movesMade == self.NUM_COLUMNS * self.NUM_ROWS:
            return True
                
        # Check if there is a winner
        if self.get_winner() != None: 
            return True

        return False
        
    def get_winner(self) -> Optional[Player]:
        color = self.get_winner_color()
        if color is None: return None
        if color == 0: return Player.FIRST
        if color == 1: return Player.SECOND
        assert False

    def get_winner_color(self) -> int:
        # Check rows
        for row in range(self.NUM_ROWS - 1, -1, -1):
            win = self.get_row_winner(row)
            if win != -1: return win
        
        # Check columns
        for col in range(self.NUM_COLUMNS):
            win = self.get_column_winner(col)
            if win != -1: return win
        
        # Check diagonals
        
        # Starting points along the top/bottom
        for col in range(self.NUM_COLUMNS - 3):
            # Main diagonal (top to bottom, left to right)
            win = self.get_diagonal_winner(0, col, True)
            if win != -1: return win
            
            # Inverse diagonal (bottom to top, left to right)
            win = self.get_diagonal_winner(self.NUM_ROWS - 1, col, False)
            if win != -1: return win
        
        # Starting points along the left
        for row in range(1, self.NUM_ROWS - 3):
            # Main diagonal (left to right, top to bottom)
            win = self.get_diagonal_winner(row, 0, True)
            if win != -1: return win
            
            # Inverse diagonal (right to left, top to bottom)
            win = self.get_diagonal_winner(self.NUM_ROWS - 1 - row, 0, False)
            if win != -1: return win
        
        return None # No winner found

    def get_possible_moves(self) -> List[ConnectFourMove]:
        moves = []
        for col in range(self.NUM_COLUMNS):
            if self.board[0][col] == -1:
                moves.append(ConnectFourMove(col))
        return moves

    def get_current_player(self) -> Player:
        return self.current_player

    def create_move_from_str(self, move_str: str) -> ConnectFourMove:
        return ConnectFourMove(int(move_str))

    def is_valid_move(self, move: ConnectFourMove) -> bool:
        return move.column >= 0 and move.column < self.NUM_COLUMNS

    def perform_move(self, move: ConnectFourMove) -> None:
        self.previous_move = move
        if self.is_valid_move(move):
            col = move.column
            for row in range(self.NUM_ROWS - 1, -1, -1):
                if self.board[row][col] == -1:
                    self.board[row][col] = self.current_player.value
                    self.movesMade += 1
                    break
            self.current_player = Player.SECOND if self.current_player == Player.FIRST else Player.FIRST

    def get_description(self) -> str:
        return self.get_display_text()

    def get_opponent_move(self) -> Optional[Move]:
        return self.previous_move

    def get_copy(self) -> Any:
        return copy.deepcopy(self)

    def get_neural_net_description_of_state(self) -> Any:
        # TODO: Implement
        pass

    def get_display_text(self):
        board_str = ""
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLUMNS):
                if col != -1:
                    board_str += '|'
                slot = self.board[row][col] if self.board[row][col] != -1 else " "
                board_str += f" {slot} "
            board_str += '\n'
            if row != self.NUM_ROWS - 1:
                board_str += '-' * (self.NUM_COLUMNS * 3 + self.NUM_COLUMNS - 1) + '\n'
        return board_str