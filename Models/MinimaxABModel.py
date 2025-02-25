from Games.Game import Game, Player
from Models.Model import Model


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
        _best, selected_move = self.minimax(0, self.game, True, self.MIN, self.MAX)
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
            return game_state.score_position(self.player), 0
     
        if maximizingPlayer: 
          
            best = self.MIN
     
            # Recur for each possible move
            moves = self.game.get_possible_moves()
            assert len(moves) > 0, "Model has no moves to select but game is not over"
            best_move = moves[0]
            # For each possible move, create a new copy of game state and make the move
            for m in moves:
                new_game_state = game_state.get_copy()
                new_game_state.perform_move(m)
                val, _move = self.minimax(depth + 1, new_game_state, False, alpha, beta) 

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
            moves = self.game.get_possible_moves()
            best_move = moves[0]
            # For each possible move, create a new copy of game state and make the move
            for m in moves:
                new_game_state = game_state.get_copy()
                new_game_state.perform_move(m)
                val, _ = self.minimax(depth + 1, new_game_state, True, alpha, beta) 

                if val < best:
                    best_move = m
                best = min(best, val) 
                
                beta = min(beta, best) 
     
                # Alpha Beta Pruning 
                if beta <= alpha: 
                    break
              
        return best, best_move