# Machine Learning State Encoding

`encode_board` converts a `Board` into a one-dimensional NumPy array for the reinforcement-learning model.

```python
state.shape == (463,)
state.dtype == np.float32
```

All indexes below are zero-based, and the end of each range is exclusive when written as a Python slice.

## Overall Layout

| Python slice | Indexes | Size | Contents |
|---|---:|---:|---|
| `state[0:3]` | 0-2 | 3 | Number of players, one-hot encoded for 2, 3, or 4 players |
| `state[3:7]` | 3-6 | 4 | Starting-player position relative to the current player |
| `state[7:13]` | 7-12 | 6 | Gem counts in the bank |
| `state[13:16]` | 13-15 | 3 | Remaining cards in levels 1, 2, and 3 decks |
| `state[16:196]` | 16-195 | 180 | Twelve visible market cards |
| `state[196:231]` | 196-230 | 35 | Five noble tiles |
| `state[231:289]` | 231-288 | 58 | Current player |
| `state[289:347]` | 289-346 | 58 | Next player |
| `state[347:405]` | 347-404 | 58 | Next-next player |
| `state[405:463]` | 405-462 | 58 | Next-next-next player or zero padding |

The total is:

```text
3 + 4 + 6 + 3 + 180 + 35 + (4 * 58) = 463
```

## Global Features

### Player Count: `state[0:3]`

One-hot encoding in this order:

```text
[2 players, 3 players, 4 players]
```

Examples:

```text
2 players -> [1, 0, 0]
3 players -> [0, 1, 0]
4 players -> [0, 0, 1]
```

### Starting Position: `state[3:7]`

One-hot encoding of the starting player’s position relative to the current player:

```text
[current player, next player, next-next player, next-next-next player]
```

The player order is rotated so that the current turn player is always the first player block.

### Bank Gems: `state[7:13]`

Values are stored in this order:

```text
[white, blue, black, red, green, gold]
```

Colored gems are divided by `MAX_BANK_COLORED_GEMS` (`7`). Gold is divided by `MAX_GOLD` (`5`). Values are capped at `1.0`.

### Remaining Deck Cards: `state[13:16]`

Values are stored in this order:

```text
[level 1 deck, level 2 deck, level 3 deck]
```

Each value is divided by `40`, then capped at `1.0`.

## Card Encoding

Each card uses 15 consecutive values. The market contains 12 cards, so it uses `12 * 15 = 180` values.

### One Card: `15` values

| Offset | Size | Contents |
|---:|---:|---|
| 0 | 1 | Presence flag |
| 1-3 | 3 | Card level, one-hot for levels 1, 2, and 3 |
| 4-8 | 5 | Card color, one-hot for W, U, B, R, and G |
| 9 | 1 | Victory points divided by `MAX_CARD_POINTS` (`5`) |
| 10-14 | 5 | Costs in white, blue, black, red, and green |

The five cost values are each divided by `MAX_CARD_COST` (`7`) and capped at `1.0`.

An empty card slot is encoded as fifteen zeroes.

### Market Cards: `state[16:196]`

Cards appear in deck order, then field order:

```text
level 1, field slots 0-3
level 2, field slots 0-3
level 3, field slots 0-3
```

For a card at market position `market_index`, its starting index is:

```python
card_start = 16 + market_index * 15
```

## Noble Tiles: `state[196:231]`

Five tile slots use seven values each. Tiles are sorted by points and then by their requirements before encoding.

### One Noble Tile: `7` values

| Offset | Size | Contents |
|---:|---:|---|
| 0 | 1 | Presence flag |
| 1 | 1 | Victory points divided by `MAX_CARD_POINTS` (`5`) |
| 2-6 | 5 | Requirements in white, blue, black, red, and green |

Requirements are divided by `MAX_CARD_COST` (`7`) and capped at `1.0`.

If fewer than five nobles remain, unused slots are filled with zeroes.

## Player Blocks

Each player uses 58 values. Players are encoded from the current player’s perspective:

```text
player block 0: current player
player block 1: next player
player block 2: next-next player
player block 3: next-next-next player
```

For games with fewer than four players, unused player blocks are filled with zeroes.

### One Player: `58` values

| Relative offset | Size | Contents |
|---:|---:|---|
| 0 | 1 | Total victory points |
| 1-5 | 5 | Colored gems: W, U, B, R, G |
| 6 | 1 | Gold gems |
| 7-11 | 5 | Permanent card bonuses: W, U, B, R, G |
| 12 | 1 | Number of owned noble tiles |
| 13-57 | 45 | Three reserved cards |

Points are divided by `MAX_PLAYER_POINTS` (`15`). Colored gems are divided by `MAX_COLORED_GEMS` (`10`). Gold is divided by `MAX_GOLD` (`5`). Permanent card bonuses are divided by `MAX_CARD_COST` (`7`). All values are capped at `1.0`.

Each reserved card uses the same 15-value card encoding described above. An unused hand slot is filled with zeroes.

For player block `relative_player_index`, its starting index is:

```python
player_start = 231 + relative_player_index * 58
```

## Normalization Summary

| Data | Normalization constant |
|---|---:|
| Card points | `MAX_CARD_POINTS = 5` |
| Card and noble costs | `MAX_CARD_COST = 7` |
| Player points | `MAX_PLAYER_POINTS = 15` |
| Player colored gems | `MAX_COLORED_GEMS = 10` |
| Bank colored gems | `MAX_BANK_COLORED_GEMS = 7` |
| Gold gems | `MAX_GOLD = 5` |

Every normalized numeric feature is capped at `1.0`.

## Important Perspective Rule

The encoder does not preserve the original player indexes. It rotates the players so the player whose turn it is appears first. This means the model can always interpret the first player block as the acting player, regardless of the original `board.turn_player` value.
