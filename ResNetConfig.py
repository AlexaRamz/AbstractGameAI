import torch
from dataclasses import dataclass

@dataclass
class ResNetConfig:
	num_resBlocks: int
	num_hidden: int
	device: torch.device
	models_folder: str
	model_path: str

connectfour_resNet_config = ResNetConfig(
	num_resBlocks = 2,
	num_hidden = 128,
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
	models_folder = "models_connectfour",
	model_path = "models_connectfour/model_0.pt"
)

chess_resNet_config = ResNetConfig(
	num_resBlocks = 10,
	num_hidden = 128,
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
	models_folder = "models_chess",
	model_path = "model_0.pt"
)
