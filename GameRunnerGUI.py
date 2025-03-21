from GameSelectionGUI import GameSelectionGUI
from ConnectFourGUI import ConnectFourGUI

from Games.Game import Player
from Games.ConnectFour import ConnectFour

from Models.HumanModel import HumanModel
from Models.Minimax import Minimax
from Models.MCTS import MCTS

import threading
import queue


class GameRunnerGUI:
    def __init__(self):
        self.main_menu = GameSelectionGUI(self)
        self.game_view = None

        self.game = None
        self.game_stopped = False

        self.player_one = HumanModel()
        self.player_two = None

        self.board_queue = queue.Queue()

        self.player1_move = ""
        self.player_input_event = threading.Event()

        self._stop_event = threading.Event()

        self.main_menu.create_window()

    def start_game(self, board_queue):
        self.board_queue = board_queue
        if self.game and self.player_one and self.player_two:
            self.player_one.set_game_and_player(self.game, Player.FIRST)
            self.player_two.set_game_and_player(self.game, Player.SECOND)

            self.next_turn()

    def next_turn(self):
        if not self._stop_event.is_set():
            self.update_game_view()
            if not self.game.is_game_over():
                current = self.game.get_current_player()
                if current == Player.SECOND:
                    print("Waiting for player 2 input...")
                    self.player_two.take_move()
                    self.next_turn()
                else:
                    print("Waiting for player 1 input...")
                    while not self.game_stopped:
                        self.player_input_event.clear()
                        self.player_input_event.wait()
                        self.player_input_event.clear()

                        success = self.handle_player_move(self.player1_move)
                        if success:
                            break
                    self.next_turn()
            else:
                if self.game.get_winner() == Player.FIRST:
                    self.game_view.display_win("You win!")
                else:
                    self.game_view.display_win("Player 2 wins!")

    def set_player_move(self, move: str):
        self.player1_move = move
        self.player_input_event.set()

    def handle_player_move(self, move: str):
        if self.game.current_player == Player.FIRST:
            return self.game.perform_move_from_str(move)
        return False

    def select_game(self, game: str):
        if game == "Connect4":
            self.game = ConnectFour()
            self.game_view = ConnectFourGUI(self)
        elif game == "Chess":
            return
        else:
            return

    def select_opponent(self, game: str):
        if game == "Minimax":
            self.player_two = Minimax()
        elif game == "MCTS":
            self.player_two = MCTS()

        self.main_menu.close_window()
        self.start_game_gui()

    def get_games(self):
        return ["Connect4", "Chess"]

    def get_opponents(self):
        return ["Minimax", "MCTS"]

    def start_game_gui(self):
        # Use threading to allow background process (game loop and move computation) and GUI to run at the same time
        thread = threading.Thread(
            target=self.start_game, args=(self.board_queue,))
        thread.daemon = True
        thread.start()
        self.game_view.run_window(self.board_queue)

    def update_game_view(self):
        self.board_queue.put(self.game.board)


def main():
    GameRunnerGUI()


if __name__ == "__main__":
    main()
