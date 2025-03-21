# Abstract Game AI
## Set up environment
To run our program, make sure you have the following packages installed:
- PyTorch
- NumPy
- python-chess

## Test AI models
Pit two models of your choice against each other in the game of your choice, or play against an AI yourself! See the game play out in the command interface.
Run GameRunner.py directly using a command with this format:

`python main.py [game] [player 1] [player 2]`

e.g. to play chess against Minimax as the first player, use the command

`python main.py chess human minimax`

All games:
- connect4
- chess
  
All players:
- human (you)
- random
- minimax
- mcts
- alphazero (not yet implemented for chess)

## Play Connect4 GUI
Play Connect4 against our Minimax, MCTS, and Alpha Zero models in a graphical interface! 

Simply run ConnectFourGUI.py and select your opponent.

![image](https://github.com/user-attachments/assets/643a7158-8e7b-43ed-b590-5539cd3a651f)
