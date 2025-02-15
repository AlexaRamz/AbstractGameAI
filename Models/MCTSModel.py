from Games.Game import Game, Player, Move
from Models.Model import Model
from typing import Optional, Dict
import random
import math

class MCTSNode:

    def __init__(self, game_state: Game, move: Optional[Move], parent: Optional["MCTSNode"]):
        self.game_state = game_state
        self.parent = parent
        self.visit_count = 0
        self.move = move
        self.win_count = 0
        self.unexplored_moves = game_state.get_possible_moves()
        self.children: Dict[Move: "MCTSNode"] = {}

    def is_fully_expanded(self) -> bool:
        return len(self.unexplored_moves) == 0

    def best_child(self):
        exploration_weight: float = 1.414
        return max(
            self.children.values(),
            key=lambda child: (child.win_count / (child.visit_count + 1e-6)) + exploration_weight * math.sqrt(
                math.log(self.visit_count + 1) / (child.visit_count + 1e-6)
            )
        )

    def expand(self):
        move = self.unexplored_moves.pop()
        new_game_state = self.game_state.get_copy()
        new_game_state.perform_move(move)
        new_node = MCTSNode(new_game_state, move=move, parent=self)
        self.children[move] = new_node
        return new_node

    def update(self, win: bool):
        self.visit_count += 1
        if win: self.win_count += 1


class MCTSModel(Model):

    def __init__(self):
        self.game = None
        self.player = None
        self.root: MCTSNode = None

    def set_game_and_player(self, game: Game, player: Player):
        self.game = game
        self.player = player
        self.root = MCTSNode(game, move=None, parent=None)

    def take_move(self):
        assert(self.game.get_current_player() == self.player)
        opp_move = self.game.get_opponent_move()
        if opp_move:
            if opp_move in self.root.children.keys():
                self.root = self.root.children[opp_move]
            else:
                self.root = MCTSNode(self.game, move=opp_move, parent=None)
        move = self.search()
        self.game.perform_move(move)
        self.root = self.root.children[move]

    def search(self, iterations: int = 500) -> Move:
        for _ in range(iterations):
            node = self.root
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
            if node.game_state.get_winner() is None and node.unexplored_moves:
                node = node.expand()
            winner = self.simulate(node.game_state)
            self.backpropagate(node, winner)
        return max(self.root.children, key=lambda move: self.root.children[move].visit_count)

    def simulate(self, game: Game) -> Optional[Player]:
        game_copy = game.get_copy()
        while game_copy.get_winner() is None:
            possible_moves = game_copy.get_possible_moves()
            if not possible_moves:
                break
            game_copy.perform_move(random.choice(possible_moves))
        return game_copy.get_winner()

    def backpropagate(self, node: MCTSNode, winner: Optional[Player]):
        while node is not None:
            node.update(winner != node.game_state.get_current_player())
            node = node.parent

    # for debugging
    def print(self, node: MCTSNode, indent = 0):
        print("--"*indent
              + str(node.move) + " "
              + ("First" if (node.game_state.get_current_player() == Player.FIRST) else "Second") + " "
              + str(node.win_count) + "/" + str(node.visit_count)
        )
        for child in node.children.values():
            self.print(child, indent + 1)
