import tkinter as tk
from Games.Game import Player
from Games.ConnectFour import ConnectFour
import queue

NUM_ROWS = 6
NUM_COLUMNS = 7

SPACING = 10
CIRCLE_RADIUS = 30
MARGIN = 10

class ConnectFourGUI:
  def __init__(self, controller):
    self.controller = controller

    self.root = None
    self.canvas = None

    self.board_queue = None

  def run_window(self, board_queue):
    self.board_queue = board_queue
    self.create_window()

  def create_window(self):
    self.root = tk.Tk()
    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    width = 2 * MARGIN + NUM_COLUMNS * (2 * CIRCLE_RADIUS + SPACING)
    height = 2 * MARGIN + NUM_ROWS * (2 * CIRCLE_RADIUS + SPACING)
    self.root.geometry(str(width) + "x" + str(height))
    self.root.title("Connect4")

    self.canvas = tk.Canvas(self.root, bg="blue")
    self.canvas.pack(fill="both", expand=True)

    self.canvas.bind("<Button-1>", self.click_handler)

    self.update_gui()
    self.root.mainloop()

  def update_gui(self):
    try:
        board_data = self.board_queue.get_nowait()
        self.update_board(board_data)
        print("update")
    except queue.Empty:
        pass
    self.root.after(10, self.update_gui)

  def click_handler(self, event):
    x = event.x
    column_width = 2 * CIRCLE_RADIUS + SPACING

    for col in range(NUM_COLUMNS):
      left = col * column_width
      right = left + column_width
      if x >= left and x < right:
        self.select_column(col)
  
  def select_column(self, column):
    self.controller.set_player_move(str(column))

  def update_board(self, board_data):
    self.canvas.delete("all")

    for row in range(NUM_ROWS):
      for col in range(NUM_COLUMNS):
        x = MARGIN + col * (2 * CIRCLE_RADIUS + SPACING)
        y = MARGIN + row * (2 * CIRCLE_RADIUS + SPACING)

        # Determine the color of the slot based on the player piece
        color = "black" # Empty slot
        piece = board_data[row, col]
        if piece == Player.FIRST.value:
          color = "red"
        elif piece == Player.SECOND.value:
          color = "yellow"

        self.canvas.create_oval(x, y, x + 2 * CIRCLE_RADIUS, y + 2 * CIRCLE_RADIUS, fill=color, outline="")

  def display_win(self, text):
    # TODO
    print(text)

  def close_window(self):
    self.root.destroy()

  def on_closing(self):
    self.controller.stop_game()
