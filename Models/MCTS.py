import math
import random
from typing import Tuple, Optional, Dict, List

from Games.Game import Game, Player, Move
from Models.Model import Model

class Node:
    def __init__(self, unexpanded_moves: List[Move], next_player_to_play: Player, parent: Optional["Node"] = None, move: Optional[Move] = None):
        self.win_count = 0
        self.visit_count = 0
        self.parent = parent
        self.move = move
        self.next_player_to_play = next_player_to_play
        self.children: Dict[Move: "Node"] = {}
        self.unexpanded_moves = unexpanded_moves
        random.shuffle(unexpanded_moves)

class MCTS(Model):

    def __init__(self, iterations_per_move: int = 500):
        self.game: Game = None
        self.player: Player = None
        self.root: Node = None
        self.iterations_per_move = iterations_per_move

    def set_game_and_player(self, game: Game, player: Player):
        self.game = game
        self.player = player
        self.root = Node(game.get_possible_moves(), player)

    def take_move(self):
        assert(self.game.get_current_player() == self.player)
        # Apply opponent move
        opp_move = self.game.get_opponent_move()
        if opp_move:
            if opp_move in self.root.children.keys():
                self.root = self.root.children[opp_move]
                self.root.parent = None
            else:
                self.root = Node(self.game.get_possible_moves(), self.player, None, opp_move)
        # Iterations
        game_state_copy = self.game.get_copy()
        for _ in range(self.iterations_per_move):
            self.do_iteration(game_state_copy)
        # Select
        self.root = self.most_visited_child_of_node(self.root)
        self.game.perform_move(self.root.move)

    def do_iteration(self, game_state):
        undo_count = 0
        # Selection
        node = self.root
        while node.children and len(node.unexpanded_moves) == 0:
            node = self.best_child_of_node(node)
            undo_count += 1
            game_state.perform_move(node.move)
        # Expansion
        if node.unexpanded_moves:
            move = node.unexpanded_moves.pop()
            undo_count += 1
            game_state.perform_move(move)
            node = Node(game_state.get_possible_moves(), self.opposite_player(node.next_player_to_play), node, move)
            node.parent.children[move] = node
        # Simulation
        while not game_state.is_game_over():
            moves = game_state.get_possible_moves()
            move = random.choice(moves)
            undo_count += 1
            game_state.perform_move(move)
        winner = game_state.get_winner()
        # Backpropagation
        while node:
            node.visit_count += 1
            if node.next_player_to_play == winner:
                node.win_count += 1
            node = node.parent
        for _ in range(undo_count):
            game_state.undo_move()

    def best_child_of_node(self, node: Node) -> Node:
        exploration_param = math.sqrt(2)
        best_score = -1
        best_child = None
        for child in node.children.values():
            exploitation = -child.win_count / child.visit_count
            exploration = math.sqrt(math.log(node.visit_count) / child.visit_count)
            score = exploitation + exploration_param * exploration
            if score > best_score or best_child == None:
                best_score = score
                best_child = child
        return best_child

    def most_visited_child_of_node(self, node: Node) -> Node:
        most_visits = 0
        most_visited_child = None
        for child in node.children.values():
            if child.visit_count > most_visits or most_visited_child == None:
                most_visits = child.visit_count
                most_visited_child = child
        return most_visited_child

    def opposite_player(self, player: Player) -> Player:
        if player == Player.FIRST: return Player.SECOND
        else: return Player.FIRST
