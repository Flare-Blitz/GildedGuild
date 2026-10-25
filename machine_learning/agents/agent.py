"""An agent designed to play the gilded guild game train the neural network.
Child components need to implement """

from abc import abstractmethod
from collections import deque
import random

import numpy as np
import torch
from machine_learning.agents.model import LinearQNet, QTrainer
from machine_learning.agents.state_encoder import INPUT_SIZE, encode_board
from machine_learning.game_files.components import Board, Player
from machine_learning.game_files.game import Game

MAX_MEMORY = 100_000
BATCH_SIZE = 128
LR = 0.001
ACTION_COUNT = 45

class Agent:
    """This defines an agent being set up from playing a game and training a Neural Network."""
    def __init__(self, total_games):
        self.total_games = total_games

        self.n_games = 0
        self.epsilon = 1.0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(INPUT_SIZE, 256, ACTION_COUNT)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_board_state(self, board: Board) -> np.ndarray:
        """Return the current board from the acting player's perspective."""
        return encode_board(board)

    def remember(self, state, action, reward, next_state, done):
        """Store the experience in the agent's memory."""
        # popleft if MAX_MEMORY is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """Train the agent on a batch of experiences."""
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """Train the agent on a single experience."""
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_training_actions(self, state):
        """Determine the action to take based on the current state."""

        self.epsilon = max(0.1, 1.0 - (self.n_games / self.total_games))
        # self.epsilon = 0
        if random.random() < self.epsilon:
            moves = list(range(ACTION_COUNT))
            random.shuffle(moves)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            moves = torch.argsort(prediction, descending=True)

        return moves

    def play_single_game(self, game: Game, players: list[Player]):
            """Play a single game and return the result."""
            result = game.training_game(players)
    
            while result is None:
                original_state = self.get_board_state(game.board)
                moves = self.get_training_actions(original_state)
                moves_attempted = 0
    
                for move in moves:
                    result, valid_move = game.take_agent_action(move)
    
                    # Create a one-hot encoded action vector to train the model
                    action = [0] * 45
                    action[move] = 1
    
                    next_state = self.get_board_state(game.board)
    
                    reward = self.evaluate_board(game.board, result, valid_move)
    
                    done = result is not None
    
                    self.train_short_memory(original_state, action, reward, next_state, done)
                    self.remember(original_state, action, reward, next_state, done)
    
                    if valid_move:
                        break
                    moves_attempted += 1
    
                if moves_attempted == len(moves):
                    # Pass the turn after verifying there are no legal actions.
                    result, valid_move = game.take_agent_action(None)
    
            return result

    @abstractmethod
    def train(self):
        """Train the model."""

    @abstractmethod
    def evaluate_board(self, board, result, move_valid):
        """Evaluate the current state of the board.
        return a numerical evaluation of the board state.
        """

    @abstractmethod
    def evaluate_model(self):
        """Evaluate the model's performance.
        Generate a plot showing the model's winrate, as well
        as any other metrics.
        """
