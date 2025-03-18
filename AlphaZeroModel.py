# Recreating DeepMind's AlphaZero (ResNet): https://www.youtube.com/playlist?list=PLkYhK7LiOk0OWeGIRsbJz8kZGWxhrTpRx
# Alpha Go Zero (Training): https://www.youtube.com/watch?v=5UYA-V2a3cc
# AlphaZero (Complete): https://www.youtube.com/watch?v=wuSQpLinRB4
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from Games.Game import Game, Player
from Models.Model import Model

class AlphaZeroModel(Model):
	def __init__(self):
		self.game = None
		self.player = None
		
		self.NN = ResNetConnect4(torch.device("cpu"))
	
	def set_game_and_player(self, game: Game, player: Player):
		self.game = game # Connect4 only!!
		self.player = None
	
	def take_move(self):
		# TODO
		pass

class ResNetConnect4(nn.Module):
	def __init__(self, device):
		super().__init__()
		self.device = device
		# define the layers themselves

		# conv
		in_channels = 3 # Passing in three boards (layers): Piece locations for player 1, player 2, and empty
		self.initial_conv = nn.Conv2d(in_channels, 128, kernel_size=3, stride=1, padding=1, bias=True)
		self.inital_bn = nn.BatchNorm2d(128)

		# Res block 1
		self.res1_conv1 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res1_bn1 = nn.BatchNorm2d(128)
		self.res1_conv2 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res1_bn2 = nn.BatchNorm2d(128)

		# Res block 2
		self.res2_conv1 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res2_bn1 = nn.BatchNorm2d(128)
		self.res2_conv2 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
		self.res2_bn2 = nn.BatchNorm2d(128)

		# Note: 12-13 residual blocks for AlphaGo. Fewer for Connect4

		# value head - Outputs number between -1 to +1 representing the value of the board state from player 1's persective
		self.value_conv = nn.Conv2d(128, 3, kernel_size=1, stride=1, bias=True)
		self.value_bn = nn.BatchNorm2d(3)
		self.value_fc = nn.Linear(3*6*7, 32) # Fully connected layer
		self.value_head = nn.Linear(32, 1)
		
		# policy head - Gives best next action
		self.policy_conv = nn.Conv2d(128, 32, kernel_size=1, stride=1, bias=True)
		self.policy_bn = nn.BatchNorm2d(32)
		self.policy_head = nn.Linear(32*6*7, 7)
		self.policy_ls = nn.LogSoftmax(dim=1) # Convert output to probabilities of choosing each action. Using instead of Softmax for training efficiency

		self.to(device)

	def forward(self, x):
		# define connections between the layers
		# x will be shape (3, 6, 7)

		# add dimension for batch size
		# * We want to pass data in batches rather than one at a time
		# * Just adds a dimension, not specifying it yet
		# * Batch size will be a hyperparameter we want to tune
		x = x.view(-1, 3, 6, 7)
		x = self.inital_bn(self.initial_conv(x))
		x = F.relu(x) # Activation function

		# Res Block 1
		res = x
		x = F.relu(self.res1_bn1(self.res1_conv1(x)))
		x = F.relu(self.res1_bn2(self.res1_conv2(x)))
		x += res
		x = F.relu(x)

		# Res Block 2
		res = x
		x = F.relu(self.res2_bn1(self.res2_conv1(x)))
		x = F.relu(self.res2_bn2(self.res2_conv2(x)))
		x += res
		x = F.relu(x)

		# Innovation of AlphaGo Zero: Combining value head and policy head into the same network, rather than having a separate value network and policy network. The distilled information needed to make both judgements is the same.
		# value head
		v = F.relu(self.value_bn(self.value_conv(x)))
		v = v.view(-1, 3*6*7)
		v = F.relu(self.value_fc(v))
		v = F.tanh(v) # Hyperbolic tangent activation function: Ensures output is in between -1 and 1

		# policy head
		p = F.relu(self.policy_bn(self.policy_conv(x)))
		p = p.view(-1, 32*6*7)
		p = F.relu(self.policy_head(p))
		p = self.policy_ls(p).exp()
		# Outputs policy: 7-valued array of numbers indicating the probabilities between 0 and 1 of choosing a given action. The highest one tells us the best action to take

		return v, p
	
if __name__ == "__main__":
	from torchinfo import summary
	device = torch.device('cpu')

	model = ResNetConnect4(device) # instantiate model
	architecture_summary = summary(model, input_size=(16,3,6,7), verbose=0) # Run a dummy tensor through the model (batch size 16)

	print(architecture_summary) 

