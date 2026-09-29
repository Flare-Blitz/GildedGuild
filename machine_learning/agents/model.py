"""
Q-Neural Network for Deep Q-Learning
"""

import os
from pathlib import Path
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
import numpy as np

class LinearQNet(nn.Module):
    """Simple feedforward neural network for Q-learning."""

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, hidden_size)
        self.linear4 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """Forward pass through the network."""
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.relu(self.linear3(x))
        x = self.linear4(x)
        return x

    def save(self, file_name='model.pth'):
        """Save the model's state dictionary to a file."""
        model_folder_path = Path(__file__).parent / 'model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

    def load(self, file_name):
        model_folder_path = Path(__file__).parent / "model"
        file_path = model_folder_path / file_name

        if file_path.is_file():
            state_dict = torch.load(file_path, weights_only=True)
            self.load_state_dict(state_dict)


class QTrainer: #pylint: disable=too-few-public-methods
    """Trainer for the Q-Network."""

    def __init__(self, model, lr, gamma):
        self.lr = lr #Learning rate
        self.gamma = gamma #Discount factor
        self.model = model #Model to be trained
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        """Perform a single training step."""
        state = np.array(state)
        next_state = np.array(next_state)
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()

        for i, d in enumerate(done):
            q_new = reward[i]
            if not d:
                q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))

            target[i][torch.argmax(action[i]).item()] = q_new

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
