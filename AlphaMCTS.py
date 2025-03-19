# Alpha Zero (complete): https://www.youtube.com/watch?v=wuSQpLinRB4
from typing import Optional, Dict
import math
import random
import numpy as np
import torch

from Games.Game import Game, Player, Move

class MCTSNode:
    def __init__(self, game_state: Game, args, action_taken: int=None, parent: Optional["MCTSNode"]=None, prior=0):
        self.game_state = game_state
        self.args = args
        self.parent = parent
        self.action_taken = action_taken
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
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = child.value_sum / child.visit_count
            if child.game_state.get_current_player() == Player.FIRST:
                q_value = -q_value
        return q_value + self.args["exploration_weight"] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

    def expand(self, policy):
        for action_taken, prob in enumerate(policy):
            move = self.game_state.get_move_by_index(action_taken)
            if move in self.game_state.get_possible_moves():
                child_state = self.game_state.get_copy()
                child_state.perform_move(move)
                child = MCTSNode(child_state, self.args, action_taken, self, prob)
                self.children[move] = child

    def update(self, value):
        self.value_sum += value
        self.visit_count += 1

class AlphaMCTS():
    def __init__(self, game: Game, model, args):
        self.game = game
        self.model = model
        self.args = args
        self.root = None

    def take_move(self):
        opp_move = self.game.get_opponent_move()
        if opp_move:
            if opp_move in self.root.children.keys():
                self.root = self.root.children[opp_move]
            else:
                self.root = MCTSNode(self.game, self.args)
        action_probs = self.search(self.game)
        action_index = np.argmax(action_probs)
        move = self.game.get_move_by_index(action_index)
        self.game.perform_move(move)
        self.root = self.root.children[move]
    
    def search(self, game_state) -> Move:
        self.root = MCTSNode(game_state, self.args)
        
        for _search in range(self.args["num_searches"]):
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
                policy, value = self.model(
                    torch.tensor(node.game_state.get_neural_net_description_of_state(), device=self.model.device).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().flatten().numpy()

                # policy = [0.1, 0.1, 0.2, 0.4, 0.2, 0.1, 0.1]
                # random.shuffle(policy)
                # value = node.game_state.score_position(node.game_state.get_current_player())
                
                # Extract float value
                value = value.item()

                # Expansion
                node.expand(policy)
            
            # Backpropagation
            self.backpropagate(node, value)

        action_probs = np.zeros(self.game.get_action_size())
        for child in self.root.children.values():
            action_probs[child.action_taken] = child.visit_count

        total_prob =  np.sum(action_probs)
        if total_prob > 0:
            action_probs /= total_prob
        return action_probs

    def backpropagate(self, node: MCTSNode, value: float):
        while node is not None:
            node.update(value)
            node = node.parent
