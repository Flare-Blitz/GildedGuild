"""Generate test cases for agents/agent.py."""

# pylint: disable=missing-function-docstring

from unittest.mock import Mock, patch

import numpy as np
import torch

from machine_learning.agents.agent import Agent
from machine_learning.agents.state_encoder import encode_board


def test_agent_initialization_sets_expected_defaults():
    agent = Agent(total_games=42)

    assert agent.total_games == 42
    assert agent.n_games == 0
    assert agent.epsilon == 1.0
    assert agent.gamma == 0.97
    assert len(agent.memory) == 0
    assert agent.model is not None
    assert agent.trainer is not None


def test_save_checkpoint_passes_training_state_to_model_save():
    agent = Agent(total_games=11)
    agent.n_games = 9
    agent.epsilon = 0.42

    with patch.object(agent.model, "save") as mock_save:
        agent.save_checkpoint("checkpoint_name")

    mock_save.assert_called_once_with(
        "checkpoint_name",
        optimizer=agent.trainer.optimizer,
        epsilon=0.42,
        n_games=9,
    )


def test_load_checkpoint_updates_agent_state_from_saved_metadata():
    agent = Agent()
    checkpoint = {"epsilon": 0.35, "n_games": 15}

    with patch.object(agent.model, "load", return_value=checkpoint) as mock_load:
        with patch.object(agent.model, "train") as mock_train:
            agent.load_checkpoint("existing_checkpoint")

    mock_load.assert_called_once_with(
        "existing_checkpoint",
        required=False,
        optimizer=agent.trainer.optimizer,
    )
    assert agent.epsilon == 0.35
    assert agent.n_games == 15
    mock_train.assert_called_once_with()


def test_load_checkpoint_returns_early_when_file_is_missing():
    agent = Agent()

    with patch.object(agent.model, "load", return_value=None) as mock_load:
        with patch.object(agent.model, "train") as mock_train:
            agent.load_checkpoint("missing_checkpoint")

    mock_load.assert_called_once_with(
        "missing_checkpoint",
        required=False,
        optimizer=agent.trainer.optimizer,
    )
    assert agent.epsilon == 1.0
    assert agent.n_games == 0
    mock_train.assert_not_called()


def test_get_board_state_matches_encoder_result(board):
    agent = Agent()

    encoded = agent.get_board_state(board)
    expected = encode_board(board)

    assert isinstance(encoded, np.ndarray)
    np.testing.assert_array_equal(encoded, expected)


def test_remember_and_train_long_memory_store_and_train_experience():
    agent = Agent()
    state = np.array([1.0, 2.0, 3.0])
    next_state = np.array([4.0, 5.0, 6.0])
    experience = (state, [0, 1], 1.5, next_state, False)

    agent.remember(*experience)
    assert list(agent.memory)[0] == experience

    with patch("machine_learning.agents.agent.random.sample", return_value=[experience]):
        with patch.object(agent.trainer, "train_step") as mock_train:
            agent.train_long_memory()

    mock_train.assert_called_once()
    called_args = mock_train.call_args[0]
    assert called_args[0] == (state,)
    assert called_args[1] == ([0, 1],)
    assert called_args[2] == (1.5,)
    assert called_args[3] == (next_state,)
    assert called_args[4] == (False,)


def test_get_training_actions_explores_when_random_choice_below_epsilon():
    agent = Agent()
    legal_actions = [1, 3, 5]

    with patch("machine_learning.agents.agent.random.random", return_value=0.1):
        with patch("machine_learning.agents.agent.random.shuffle") as mock_shuffle:
            moves = agent.get_training_actions(np.array([0.0, 0.0]), legal_actions)

    assert set(moves) == set(legal_actions)
    assert len(moves) == len(legal_actions)
    mock_shuffle.assert_called_once()


def test_get_training_actions_prefers_highest_q_values_for_legal_moves():
    agent = Agent()
    legal_actions = [1, 3, 5]
    agent.model = Mock(return_value=torch.tensor([0.1, 0.8, 0.2, 0.6, 0.3, 0.9]))
    agent.n_games = 1000

    with patch("machine_learning.agents.agent.random.random", return_value=0.9):
        moves = agent.get_training_actions(np.array([0.0, 0.0]), legal_actions)

    assert moves == [5, 1, 3]
