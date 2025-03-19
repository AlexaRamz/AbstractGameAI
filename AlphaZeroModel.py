# Recreating DeepMind's AlphaZero (ResNet): https://www.youtube.com/playlist?list=PLkYhK7LiOk0OWeGIRsbJz8kZGWxhrTpRx
# Alpha Go Zero (Training): https://www.youtube.com/watch?v=5UYA-V2a3cc
# AlphaZero (Complete): https://www.youtube.com/watch?v=wuSQpLinRB4
import torch
import torch.nn.functional as F
import numpy as np
import random
from tqdm import trange

from Games.Game import Game, Player
from Models.Model import Model
from AlphaMCTS import AlphaMCTS
from ResNet import ResNet

class AlphaZeroModel(Model):
	def __init__(self):
		self.game = None
		self.player = None
		self.args = {
			'exploration_weight': 1.414,
			'num_searches': 60,
			'num_iterations': 8,
			'num_selfPlay_iterations': 10,
			'num_epochs': 4,
			'batch_size': 64
		}
		
		self.num_player1_wins = 0
		self.num_player2_wins = 0
	
	def set_game_and_player(self, game: Game, player: Player):
		self.game = game # Connect4 only right now!!
		self.player = player

		self.model = ResNet(self.game, 7, 2, torch.device('cpu'))
		self.mcts = AlphaMCTS(self.game, self.model, self.args)
		self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
	
	def take_move(self):
		assert(self.game.get_current_player() == self.player)
		self.mcts.take_move()

	def selfPlay(self):
		memory = []
		player = Player.FIRST
		state = self.game

		while True:
			print(state.get_display_text())
			action_probs = self.mcts.search(state)

			memory.append((state, action_probs, player))

			move = None
			if np.sum(action_probs) > 0:
				action_index = np.random.choice(self.game.get_action_size(), p=action_probs)
				move = self.game.get_move_by_index(action_index)
			else:
				move = random.choice(state.get_possible_moves())

			state = state.get_copy()
			state.perform_move(move)

			value, is_terminal = state.get_value_and_terminated()

			if is_terminal:
				returnMemory = []
				for hist_state, hist_action_probs, hist_player in memory:
					if value > 0: value = 1
					elif value < 0: value = -1
					hist_outcome = value
					returnMemory.append((
						hist_state.get_neural_net_description_of_state(),
						hist_action_probs,
						hist_outcome
					))
				winner = state.get_winner()
				if winner == Player.FIRST:
					self.num_player1_wins += 1
				elif winner == Player.SECOND:
					self.num_player2_wins += 1

				print(self.num_player1_wins)
				print(self.num_player2_wins)
				return returnMemory
			
			# Switch player turn
			player = Player.SECOND if player == Player.FIRST else Player.FIRST
	
	def train(self, memory):
		random.shuffle(memory)
		for batchIdx in range(0, len(memory), self.args['batch_size']):
			sample = memory[batchIdx:batchIdx+self.args['batch_size']]
			state, policy_targets, value_targets = zip(*sample)

			state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(value_targets).reshape(-1, 1)
			
			state = torch.tensor(state, dtype=torch.float32, device=self.model.device)
			policy_targets = torch.tensor(policy_targets, dtype=torch.float32, device=self.model.device)
			value_targets = torch.tensor(value_targets, dtype=torch.float32, device=self.model.device)
			
			out_policy, out_value = self.model(state)
			
			policy_loss = F.cross_entropy(out_policy, policy_targets)
			value_loss = F.mse_loss(out_value, value_targets)
			loss = policy_loss + value_loss
			
			self.optimizer.zero_grad()
			loss.backward()
			self.optimizer.step()

	def learn(self):
		for iteration in range(self.args['num_iterations']):
			memory = []
			
			self.model.eval()
			for _selfPlay_iteration in trange(self.args['num_selfPlay_iterations']):
				memory += self.selfPlay()
				
			self.model.train()
			for _epoch in trange(self.args['num_epochs']):
				self.train(memory)
			
			torch.save(self.model.state_dict(), f"model_{iteration}.pt")
			torch.save(self.optimizer.state_dict(), f"optimizer_{iteration}.pt")

if __name__ == "__main__":
	from Games.ConnectFour import ConnectFour

	alphaZero = AlphaZeroModel()
	alphaZero.set_game_and_player(ConnectFour(), Player.FIRST)
	alphaZero.learn()
