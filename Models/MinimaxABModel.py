from Games.Game import Game, Player, Move
from Models.Model import Model
from typing import List


class MinimaxABModel(Model):
    """
    Minimax with alpha-beta pruning
    """
    def __init__(self):
        self.game = None
        self.player = None
        self.MAX_DEPTH = 5

        # Initial values of Alpha and Beta 
        self.MAX, self.MIN = 1000, -1000

    def set_game_and_player(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def take_move(self):
        assert(self.game.get_current_player() == self.player)
        game_state_copy = self.game.get_copy()
        _best, selected_move = self.minimax(0, game_state_copy, True, self.MIN, self.MAX)
        self.game.perform_move(selected_move)
     
    def minimax(self, depth, game_state, maximizingPlayer, alpha, beta): 

        # Terminating condition: Game is over, or a specified max depth was reached
        if game_state.is_game_over():
            if game_state.get_winner() == self.player: # Win
                return 100, 0
            elif game_state.get_winner() == None: # Tie
                return 0, 0
            else: # Loss
                return -100, 0
        elif depth == self.MAX_DEPTH:
            score = game_state.score_position(self.player)
            if self.player == Player.SECOND:
                score *= -1 # Ensure score has consistent sign whether first or second player
            return score, 0
     
        if maximizingPlayer: 
          
            best = self.MIN
     
            # Recur for each possible move
            moves = game_state.get_possible_moves()
            assert len(moves) > 0, "Model has no moves to select but game is not over"
            best_move = moves[0]
            # Take each possible move, then undo it
            for m in moves:
                game_state.perform_move(m)
                val, _ = self.minimax(depth + 1, game_state, False, alpha, beta)
                game_state.undo_move()
                if val > best:
                    best_move = m
                best = max(best, val) 
                
                alpha = max(alpha, best) 
     
                # Alpha Beta Pruning 
                if beta <= alpha: 
                    break
          
        else:
            best = self.MAX
     
            # Recur for each possible move
            moves: List[Move] = game_state.get_possible_moves()
            best_move = moves[0]
            # Take each possible move, then undo it
            for m in moves:
                game_state.perform_move(m)
                val, _ = self.minimax(depth + 1, game_state, True, alpha, beta)
                game_state.undo_move()
                if val < best:
                    best_move = m
                best = min(best, val) 
                
                beta = min(beta, best) 
     
                # Alpha Beta Pruning 
                if beta <= alpha: 
                    break
              
        return best, best_move