"""Convert a game board into a fixed-size reinforcement-learning state."""

from __future__ import annotations

from typing import Iterable

import numpy as np

from machine_learning.game_files.components import Board, Card, Player, Tile

COLORS = ("W", "U", "B", "R", "G")
CARD_COSTS = ("white", "blue", "black", "red", "green")
MAX_PLAYERS = 4
MAX_HAND_SIZE = 3
MARKET_CARD_COUNT = 12
NOBLE_COUNT = 5

CARD_FEATURES = 15
NOBLE_FEATURES = 7
PLAYER_FEATURES = 58

PLAYER_COUNT_FEATURES = 3
STARTING_POSITION_FEATURES = MAX_PLAYERS
GLOBAL_FEATURES = (
    PLAYER_COUNT_FEATURES
    + STARTING_POSITION_FEATURES
    + 6  # bank gems, including gold
    + 3  # remaining cards in levels 1-3
    + MARKET_CARD_COUNT * CARD_FEATURES
    + NOBLE_COUNT * NOBLE_FEATURES
)
INPUT_SIZE = GLOBAL_FEATURES + MAX_PLAYERS * PLAYER_FEATURES

MAX_CARD_POINTS = 5.0
MAX_CARD_COST = 7.0
MAX_PLAYER_POINTS = 15.0
MAX_COLORED_GEMS = 10.0
MAX_GOLD = 5.0
MAX_BANK_COLORED_GEMS = 7.0


def _one_hot(value: object, choices: Iterable[object]) -> list[float]:
    """Return a one-hot encoding, or all zeroes for an unknown value."""
    return [float(value == choice) for choice in choices]


def _card_features(card: Card | None) -> list[float]:
    """Encode a card as presence, identity, points, and costs."""
    if card is None:
        return [0.0] * CARD_FEATURES

    features = [1.0]
    features.extend(_one_hot(card.level, (1, 2, 3)))

    features.extend(_one_hot(card.color, COLORS))
    features.append(min(card.points / MAX_CARD_POINTS, 1.0))
    features.extend(
        min(getattr(card, cost) / MAX_CARD_COST, 1.0)
        for cost in CARD_COSTS
    )

    return features


def _tile_features(tile: Tile | None) -> list[float]:
    """Encode a noble tile as presence, points, and requirements."""
    if tile is None:
        return [0.0] * NOBLE_FEATURES

    return [
        1.0,
        min(tile.points / MAX_CARD_POINTS, 1.0),
        *(min(getattr(tile.cost, cost) / MAX_CARD_COST, 1.0)
          for cost in CARD_COSTS),
    ]


def _player_features(player: Player) -> list[float]:
    """Encode one player's state."""
    features = [
        min(player.points / MAX_PLAYER_POINTS, 1.0),
        *(min(player.gems[color] / MAX_COLORED_GEMS, 1.0) for color in COLORS),
        min(player.gems["Au"] / MAX_GOLD, 1.0),
        *(min(player.cards[color] / MAX_CARD_COST, 1.0) for color in COLORS),
        min(len(player.tiles) / NOBLE_COUNT, 1.0),
    ]

    for hand_index in range(MAX_HAND_SIZE):
        card = player.hand[hand_index] if hand_index < len(player.hand) else None
        features.extend(_card_features(card))

    return features


def encode_board(board: Board) -> np.ndarray:
    """Return the board as a normalized, fixed-size ``float32`` array.

    Players are rotated so index zero is the current player. Missing player
    slots are zero-padded, allowing the same network to handle 2-4 players.
    """
    features: list[float] = []

    features.extend(_one_hot(board.player_count, (2, 3, 4)))
    starting_position = (
        board.starting_player - board.turn_player
    ) % board.player_count
    features.extend(_one_hot(starting_position, range(MAX_PLAYERS)))

    features.extend(
        min(board.gem_pile.gems[color] / MAX_BANK_COLORED_GEMS, 1.0)
        for color in COLORS
    )
    features.append(min(board.gem_pile.gems["Au"] / MAX_GOLD, 1.0))

    features.extend(min(len(deck.cards) / 40.0, 1.0) for deck in board.decks)

    for deck in board.decks:
        for card in deck.field:
            features.extend(_card_features(card))

    sorted_tiles = sorted(
        board.tiles.tiles,
        key=lambda tile: (
            tile.points,
            tuple(getattr(tile.cost, cost) for cost in CARD_COSTS),
        ),
    )
    for tile_index in range(NOBLE_COUNT):
        tile = sorted_tiles[tile_index] if tile_index < len(sorted_tiles) else None
        features.extend(_tile_features(tile))

    for relative_index in range(MAX_PLAYERS):
        if relative_index < board.player_count:
            player_index = (board.turn_player + relative_index) % board.player_count
            features.extend(
                _player_features(
                    board.players[player_index],
                )
            )
        else:
            features.extend([0.0] * PLAYER_FEATURES)

    state = np.asarray(features, dtype=np.float32)
    if state.shape != (INPUT_SIZE,):
        raise ValueError(f"Expected state shape {(INPUT_SIZE,)}, got {state.shape}")
    return state
