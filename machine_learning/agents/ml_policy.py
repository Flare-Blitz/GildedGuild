"""Runtime policy for players controlled by a trained Q-network."""

import torch

from machine_learning.agents.agent import ACTION_COUNT
from machine_learning.agents.model import LinearQNet
from machine_learning.agents.state_encoder import INPUT_SIZE, encode_board
from machine_learning.game_files.components import Board


class QNetworkPolicy:
    """Rank game actions using a saved Q-network."""

    def __init__(self, model: LinearQNet):
        self.model = model.eval()

    @classmethod
    def from_file(cls, file_name: str) -> "QNetworkPolicy":
        """Create a policy from weights stored in the model directory."""
        model = LinearQNet(INPUT_SIZE, 256, ACTION_COUNT)
        model.load(file_name, required=True)
        return cls(model)

    def rank_actions(
        self, board: Board,
    ) -> tuple[int, ...]:
        """Return the fixed action list ordered from highest to lowest Q-value."""
        state = torch.as_tensor(encode_board(board), dtype=torch.float32)
        with torch.inference_mode():
            q_values = self.model(state)
        action_indices = torch.argsort(q_values, descending=True).tolist()
        return action_indices
