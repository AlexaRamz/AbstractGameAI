# Recreating DeepMind's AlphaZero (ResNet): https://www.youtube.com/playlist?list=PLkYhK7LiOk0OWeGIRsbJz8kZGWxhrTpRx
# Alpha Go Zero (Training): https://www.youtube.com/watch?v=5UYA-V2a3cc
# AlphaZero (Complete): https://www.youtube.com/watch?v=wuSQpLinRB4
import torch
import torch.nn.functional as F
import numpy as np
import random
from tqdm import trange
import os

from Games.Game import Game, Player
from Models.Model import Model
from Models.AlphaZero.AlphaMCTS import AlphaMCTS
from Models.AlphaZero.ResNet import ResNet
from Models.AlphaZero.AlphaZeroConfig import AlphaZeroConfig, connectfour_config

class AlphaZeroModel(Model):
	def __init__(self, config: AlphaZeroConfig, doTraining=False):
		self.game = None
		self.player = None

		self.config = config
		self.doTraining = doTraining

	def set_game_and_player(self, game: Game, player: Player):
		self.game = game
		self.player = player

		if self.doTraining:
			self.model = ResNet(self.game, self.config.resNet_config)
			self.mcts = AlphaMCTS(self.game, self.model, self.config)
			self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
			self.learn()
		else:
			self.load_model()
		
	def load_model(self):
		self.model = ResNet(self.game, self.config.resNet_config)
		self.model.load_model()
		self.mcts = AlphaMCTS(self.game, self.model, self.config)
		self.model.eval()
	
	def take_move(self):
		assert(self.game.get_current_player() == self.player)
		self.mcts.take_move()

	def selfPlay(self):
		memory = []
		player = Player.FIRST
		state = self.game

		while True:
			# print(state.get_display_text())
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
				return returnMemory
			
			# Switch player turn
			player = Player.SECOND if player == Player.FIRST else Player.FIRST
	
	def train(self, memory):
		random.shuffle(memory)
		for batchIdx in range(0, len(memory), self.config.batch_size):
			sample = memory[batchIdx:batchIdx+self.config.batch_size]
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
		for iteration in range(self.config.num_iterations):
			memory = []
			
			self.model.eval()
			for _selfPlay_iteration in trange(self.config.num_selfPlay_iterations):
				memory += self.selfPlay()
				
			self.model.train()
			for _epoch in trange(self.config.num_epochs):
				self.train(memory)

			save_folder = self.config.resNet_config.models_folder
			if not os.path.exists(save_folder):
				os.mkdir(save_folder)
			torch.save(self.model.state_dict(), os.path.join(save_folder, f"model_{iteration}.pt"))
			torch.save(self.optimizer.state_dict(), os.path.join(save_folder, f"optimizer_{iteration}.pt"))

if __name__ == "__main__":
	from Games.ConnectFour import ConnectFour

	alphaZero = AlphaZeroModel(connectfour_config, True)
	alphaZero.set_game_and_player(ConnectFour(), Player.FIRST)
	alphaZero.learn()
