# Alpha Zero (complete): https://www.youtube.com/watch?v=wuSQpLinRB4
from typing import Optional, Dict
import math
import random
import torch

from Games.Game import Game, Player, Move

class MCTSNode:
    def __init__(self, game_state: Game, move: Optional[Move]=None, parent: Optional["MCTSNode"]=None, prior=0):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.prior = prior
        
        self.children: Dict[Move: "MCTSNode"] = {}

        self.visit_count = 0
        self.value_sum = 0

    def is_fully_expanded(self) -> bool:
        return len(self.children) > 0

    def best_child(self):
        return max(
            self.children.values(),
            key=lambda child: self.get_ucb(child)
        )
    
    def get_ucb(self, child):
        exploration_weight: float = 1.414

        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = child.value_sum / child.visit_count
            if child.game_state.get_current_player() == Player.FIRST:
                q_value = -q_value
        return q_value + exploration_weight * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

    def expand(self, policy):
        for actionIndex, prob in enumerate(policy):
            move = self.game_state.get_move_by_index(actionIndex)
            if move in self.game_state.get_possible_moves():
                child_state = self.game_state.get_copy()
                child_state.perform_move(move)
                child = MCTSNode(child_state, move, self, prob)
                self.children[move] = child

    def update(self, value):
        self.value_sum += value
        self.visit_count += 1

class AlphaMCTS():
    def __init__(self, model, game: Game):
        self.game = game
        self.model = model
        self.root = MCTSNode(game, move=None, parent=None)

    def take_move(self):
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
        self.root = MCTSNode(self.game)
        
        for i in range(iterations):
            node = self.root

            # Selection
            while node.is_fully_expanded():
                node = node.best_child()
            
            value = 0
            if node.game_state.is_game_over(): # Is terminal node
                winner = node.game_state.get_winner()
                if winner == Player.FIRST:
                    value = 10000
                elif winner == Player.SECOND:
                    value = -10000
            else:
                value, policy = self.model.forward(self.game.get_neural_net_description_of_state()) # TODO
                # policy = [0.1, 0.1, 0.2, 0.4, 0.2, 0.1, 0.1]
                # random.shuffle(policy)
                # value = node.game_state.score_position(node.game_state.get_current_player())

                # Expansion
                node.expand(policy)
            
            # Backpropagation
            self.backpropagate(node, value)

        return max(self.root.children, key=lambda move: self.root.children[move].visit_count)

    def backpropagate(self, node: MCTSNode, value: float):
        while node is not None:
            node.update(value)
            node = node.parent
