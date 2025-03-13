import tkinter as tk

class GameSelectionGUI:
  def __init__(self, controller):
    self.controller = controller

    self.root = None
    self.game_select_frame = None
    self.opponent_select_frame = None

    self.frames = []
    
  def create_window(self):
    self.root = tk.Tk()

    self.root.geometry("500x500")
    self.root.title("Game Selection")

    self.game_select_frame = tk.Frame(self.root)
    self.opponent_select_frame = tk.Frame(self.root)

    self.frames = [
      self.game_select_frame,
      self.opponent_select_frame,
    ]

    self.create_game_select_frame(),
    self.create_opponent_select_frame(),

    self.show_game_selection()

    self.root.mainloop()

  def create_game_select_frame(self):
    label = tk.Label(self.game_select_frame, text="Select a game to play", font=("Arial", 18))
    label.pack(padx=10, pady=20)

    games = self.controller.get_games()
    for game in games:
      game_btn = tk.Button(self.game_select_frame, text=game, font=("Arial", 18), command=lambda g=game: self.select_game(g))
      game_btn.pack()

  def create_opponent_select_frame(self):
    label = tk.Label(self.opponent_select_frame, text="Choose your opponent", font=("Arial", 18))
    label.pack(padx=10, pady=20)

    opponents = self.controller.get_opponents()
    for opponent in opponents:
      opponent_btn = tk.Button(self.opponent_select_frame, text=opponent, font=("Arial", 18), command=lambda opp=opponent: self.select_opponent(opp))
      opponent_btn.pack()

    back_btn = tk.Button(self.opponent_select_frame, text="Back", font=("Arial", 18), command=self.show_game_selection)
    back_btn.pack(pady=20)

  def clear_frames(self):
    for frame in self.frames:
      frame.forget()

  def show_game_selection(self):
    self.clear_frames()
    self.game_select_frame.pack(fill="both", expand=True)

  def show_opponent_selection(self):
    self.clear_frames()
    self.opponent_select_frame.pack(fill="both", expand=True)

  def select_game(self, game):
    self.controller.select_game(game)
    self.show_opponent_selection()
  
  def select_opponent(self, opponent):
    self.controller.select_opponent(opponent)

  def close_window(self):
    self.root.destroy()
