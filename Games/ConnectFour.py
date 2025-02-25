from typing import Any, List, Optional
from Games.Game import Game, Player, Move
import copy
import numpy as np

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

EMPTY = -1
NUM_ROWS, NUM_COLUMNS = 6, 7
WINDOW_LENGTH = 4

# Scores
WIN_SCORE = 100
CENTER_MULTIPLIER = 3
CONNECT_THREE = 5
CONNECT_TWO = 2
OPPONENT_THREE = -4

class ConnectFour(Game):
    
    def __init__(self):
        self.previous_move = None
        self.board = np.full((NUM_ROWS, NUM_COLUMNS), EMPTY)
        self.current_player = Player.FIRST
        self.movesMade = 0

    def is_game_over(self):    
        # Check if no more moves can be made
        if self.movesMade == NUM_COLUMNS * NUM_ROWS:
            return True
                
        # Check if there is a winner
        if self.get_winner() != None: 
            return True

        return False

    # Adapted from https://roboticsproject.readthedocs.io/en/latest/ConnectFourAlgorithm.html
    # https://github.com/kupshah/Connect-Four/blob/master/board.py
    def score_position(self, piece: Player) -> int:
        # Score the board positions for the current player
        score = 0

        # Place greater importance on moves in the center column
        center_array = self.board[:, NUM_COLUMNS // 2]
        center_count = np.sum(center_array == piece.value)
        score += center_count * 3

        # Score horizontal positions
        for r in range(NUM_ROWS):
            for c in range(NUM_COLUMNS - 3):
                # Create a horizontal window of 4
                window = self.board[r, c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)
    
        # Score vertical positions
        for c in range(NUM_COLUMNS):
            for r in range(NUM_ROWS - 3): # 
                # Create a vertical window of 4
                window = self.board[r:r + WINDOW_LENGTH, c]
                score += self.evaluate_window(window, piece)
    
        # Score positive diagonals
        for r in range(NUM_ROWS - 3):
            for c in range(NUM_COLUMNS - 3):
                # Create a positive diagonal window of 4
                window = np.array(self.board[r + i][c + i] for i in range(WINDOW_LENGTH))
                score += self.evaluate_window(window, piece)
    
        # Score negative diagonals
        for r in range(NUM_ROWS - 3):
            for c in range(NUM_COLUMNS - 3):
                # Create a negative diagonal window of 4
                window = np.array(self.board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH))
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece: Player):
        score = 0

        # Switch scoring based on turn
        opp_piece = Player.FIRST
        if piece == Player.FIRST:
            opp_piece = Player.SECOND

        piece_count = np.sum(window == piece.value)
        empty_count = np.sum(window == EMPTY)
        opp_count = np.sum(window == opp_piece.value)

        # Prioritise a winning move
        # Minimax makes this less important
        if piece_count == 4:
            score += WIN_SCORE
        # Make connecting 3 second priority
        elif piece_count == 3 and empty_count == 1:
            score += CONNECT_THREE
        # Make connecting 2 third priority
        elif piece_count == 2 and empty_count == 2:
            score += CONNECT_TWO
        # Prioritise blocking an opponent's winning move (but not over bot winning)
        # Minimax makes this less important
        if opp_count == 3 and empty_count == 1:
            score += OPPONENT_THREE

        return score

    def get_window_winner(self, window) -> Optional[Player]:
        if np.sum(window == Player.FIRST.value) == 4: return Player.FIRST
        elif np.sum(window == Player.SECOND.value) == 4: return Player.SECOND
        return None
        
    def get_winner(self) -> Optional[Player]:
        # Check rows
        for r in range(NUM_ROWS):
            for c in range(NUM_COLUMNS - 3):
                # Create a horizontal window of 4
                window = self.board[r, c:c + WINDOW_LENGTH]
                winner = self.get_window_winner(window)
                if winner is not None: return winner
    
        # Check columns
        for c in range(NUM_COLUMNS):
            for r in range(NUM_ROWS - 3): # 
                # Create a vertical window of 4
                window = self.board[r:r + WINDOW_LENGTH, c]
                winner = self.get_window_winner(window)
                if winner is not None: return winner
    
        # Check positive diagonals
        for r in range(NUM_ROWS - 3):
            for c in range(NUM_COLUMNS - 3):
                # Create a positive diagonal window of 4
                window = np.array([self.board[r + i][c + i] for i in range(WINDOW_LENGTH)])
                winner = self.get_window_winner(window)
                if winner is not None: return winner
    
        # Check negative diagonals
        for r in range(NUM_ROWS - 3):
            for c in range(NUM_COLUMNS - 3):
                # Create a negative diagonal window of 4
                window = np.array([self.board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)])
                winner = self.get_window_winner(window)
                if winner is not None: return winner
                    
        return None

    def get_possible_moves(self) -> List[ConnectFourMove]:
        moves = []
        for col in range(NUM_COLUMNS):
            if self.board[0][col] == EMPTY:
                moves.append(ConnectFourMove(col))
        return moves

    def get_current_player(self) -> Player:
        return self.current_player

    def perform_move_from_str(self, move_str: str) -> bool:
        if move_str.isdigit():
            column = int(move_str)
            if column >= 0 and column < NUM_COLUMNS:
                success = self.perform_move(ConnectFourMove(column))
                return success
        return False

    def perform_move(self, move: ConnectFourMove) -> bool:
        assert move.column >= 0 and move.column < NUM_COLUMNS

        col = move.column
        for row in range(NUM_ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = self.current_player.value
                self.movesMade += 1
                self.previous_move = move
                self.current_player = Player.SECOND if self.current_player == Player.FIRST else Player.FIRST
                return True
        return False

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
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS):
                if col != EMPTY:
                    board_str += '|'
                slot = self.board[row][col] if self.board[row][col] != EMPTY else " "
                board_str += f" {slot} "
            board_str += '\n'
            if row != NUM_ROWS - 1:
                board_str += '-' * (NUM_COLUMNS * 3 + NUM_COLUMNS - 1) + '\n'
        return board_str