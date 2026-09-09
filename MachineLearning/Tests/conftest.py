"""fixtures for testing the game module"""

# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylance: reportUnusedParameter=false

from pathlib import Path

import pytest

from MachineLearning.GameFiles.game import (
    Action,
    ActionType,
    Board,
    Card,
    Cost,
    Deck,
    Game,
    GemPile,
    Player,
    Tile,
    TileDeck,
)


@pytest.fixture
def repository_root():
    """Return the repository root used by the relative JSON data paths."""
    return Path(__file__).resolve().parents[2]


@pytest.fixture
def deterministic_random(monkeypatch):
    """Make deck order and starting-player selection predictable."""
    monkeypatch.setattr("MachineLearning.GameFiles.game.random.shuffle", lambda items: None)
    monkeypatch.setattr("MachineLearning.GameFiles.game.random.randint", lambda start, end: start)


@pytest.fixture
def game_files_cwd(monkeypatch, repository_root):
    """Run fixtures that load JSON data from the repository root."""
    monkeypatch.chdir(repository_root)


@pytest.fixture
def cost():
    """Provide a cost with one of each colored gem."""
    return Cost(white=1, blue=1, black=1, red=1, green=1)


@pytest.fixture
def card():
    """Provide a low-cost level-one card."""
    return Card(level=1, color="W", points=1, white=1, blue=1)


@pytest.fixture
def expensive_card():
    """Provide a card whose cost requires several resources"""
    return Card(
        level=2,
        color="R",
        points=3,
        white=3,
        blue=2,
        black=2,
        red=1,
        green=2,
    )


@pytest.fixture
def tile(cost):
    """Provide a noble tile with requirements in every color."""
    return Tile(points=3, cost=cost)


@pytest.fixture
def player():
    """Provide a fresh player with empty resources and collections."""
    return Player()


@pytest.fixture
def player_with_resources(player):
    """Provide a player with colored gems, gold, discounts, and points."""
    player.gems.update({"W": 2, "U": 2, "B": 2, "R": 2, "G": 2, "Au": 2})
    player.cards.update({"W": 1, "U": 1, "B": 1, "R": 1, "G": 1})
    player.points = 5
    return player


@pytest.fixture
def gem_pile():
    """Provide a four-player gem bank."""
    return GemPile(player_count=4)


@pytest.fixture
def level_one_deck(game_files_cwd, deterministic_random):
    """Provide a deterministic level-one deck with four field cards."""
    return Deck(level=1)


@pytest.fixture
def tile_deck(game_files_cwd, deterministic_random):
    """Provide a deterministic tile deck containing three nobles."""
    return TileDeck(cards=3)


@pytest.fixture
def board(game_files_cwd, deterministic_random):
    """Provide a deterministic four-player board with loaded game data."""
    return Board(player_count=4)


@pytest.fixture
def game(game_files_cwd, deterministic_random):
    """Provide a game without entering its interactive play loop."""
    return Game(player_count=4)


@pytest.fixture
def take_gems_action():
    """Provide an action for taking three differently colored gems."""
    return Action(action_type=ActionType.TAKE_GEMS, colors=("W", "U", "G"))


@pytest.fixture
def buy_board_card_action():
    """Provide an action for buying a card from level one, row one."""
    return Action(action_type=ActionType.BUY_BOARD_CARD, level=1, row=1)


@pytest.fixture
def buy_hand_card_action():
    """Provide an action for buying the first card in a player's hand."""
    return Action(action_type=ActionType.BUY_HAND_CARD, row=1)


@pytest.fixture
def reserve_card_action():
    """Provide an action for reserving level two, row one."""
    return Action(action_type=ActionType.RESERVE_CARD, level=2, row=1)

