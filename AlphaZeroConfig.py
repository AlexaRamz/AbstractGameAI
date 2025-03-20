from dataclasses import dataclass

from ResNetConfig import ResNetConfig, connectfour_resNet_config, chess_resNet_config

@dataclass
class AlphaZeroConfig:
	exploration_weight: float
	num_searches: int
	num_iterations: int
	num_selfPlay_iterations: int
	num_epochs: int
	batch_size: int
	resNet_config: ResNetConfig

connectfour_config = AlphaZeroConfig(
	exploration_weight = 1.414,
	num_searches = 200,
	num_iterations = 4,
	num_selfPlay_iterations = 200,
	num_epochs = 4,
	batch_size = 64,
	resNet_config = connectfour_resNet_config
)

chess_config = AlphaZeroConfig(
	exploration_weight = 1.414,
	num_searches = 60,
	num_iterations = 8,
	num_selfPlay_iterations = 10,
	num_epochs = 4,
	batch_size = 64,
	resNet_config = chess_resNet_config
)
