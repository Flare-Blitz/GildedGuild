"""Tests for the game.py logic."""

# pylint: disable=missing-function-docstring

# Taking Gems

def test_take_two_gems(board):
    # Arrange: start with the deterministic bank and an empty current player's reserve.
    current_player = board.players[board.turn_player]
    starting_bank = board.gem_pile.gems["W"]

    # Act: take two gems of the same color.
    result = board.take_2_gems("W")

    # Assert: two gems move from the bank to the current player.
    assert result == (True, "")
    assert board.gem_pile.gems["W"] == starting_bank - 2
    assert current_player.gems["W"] == 2


def test_take_three_gems(board, take_gems_action):
    # Arrange: use the three different colors supplied by the action fixture.
    current_player = board.players[board.turn_player]
    starting_bank = {
        color: board.gem_pile.gems[color] for color in take_gems_action.colors
    }

    # Act: take one gem from each selected pile.
    result = board.take_3_gems(*take_gems_action.colors)

    # Assert: each selected pile loses one gem and the player gains one.
    assert result == (True, "")
    for color in take_gems_action.colors:
        assert board.gem_pile.gems[color] == starting_bank[color] - 1
        assert current_player.gems[color] == 1


def test_take_two_gems_fails_when_pile_has_fewer_than_four(board):
    # Arrange: reduce the selected pile below the four-gem requirement.
    current_player = board.players[board.turn_player]
    board.gem_pile.gems["W"] = 3
    starting_player_gems = current_player.gems["W"]

    # Act: try to take two gems from the smaller pile.
    result = board.take_2_gems("W")

    # Assert: the action fails and neither side changes.
    assert result == (False, "Selected pile has fewer than 4 gems")
    assert board.gem_pile.gems["W"] == 3
    assert current_player.gems["W"] == starting_player_gems


def test_take_three_gems_fails_when_a_pile_is_empty(board):
    # Arrange: empty one of the three selected piles.
    current_player = board.players[board.turn_player]
    board.gem_pile.gems["U"] = 0
    starting_gems = current_player.gems.copy()
    starting_bank = board.gem_pile.gems.copy()

    # Act: try to take gems including the empty pile.
    result = board.take_3_gems("W", "U", "G")

    # Assert: the action fails without changing the bank or player.
    assert result == (False, "Each selected pile must have at least one gem")
    assert board.gem_pile.gems == starting_bank
    assert current_player.gems == starting_gems

# Buying Cards


def test_buy_card_using_discounts(board, player_with_resources, card):
    # Arrange: the player's card discounts cover the card's colored costs.
    starting_gems = player_with_resources.gems.copy()
    starting_card_count = player_with_resources.cards[card.color]

    # Act: buy the card directly with the prepared player.
    result = board.buy_card(player_with_resources, card)

    # Assert: no gems are needed and the card discount increases.
    assert result == (True, "")
    assert player_with_resources.gems == starting_gems
    assert player_with_resources.cards[card.color] == starting_card_count + 1


def test_buy_card_using_gold(board, player, card):
    # Arrange: give the player enough gold to cover the card's full cost.
    player.gems["Au"] = 2
    starting_gold_in_bank = board.gem_pile.gems["Au"]

    # Act: buy the card without colored gems or discounts.
    result = board.buy_card(player, card)

    # Assert: gold pays the cost and is returned to the bank.
    assert result == (True, "")
    assert player.gems["Au"] == 0
    assert board.gem_pile.gems["Au"] == starting_gold_in_bank + 2
    assert player.cards[card.color] == 1


def test_buy_card_fails_when_player_cannot_afford_it(board, player, expensive_card):
    # Arrange: keep the player unable to pay for the expensive card.
    starting_gems = player.gems.copy()
    starting_cards = player.cards.copy()
    starting_bank = board.gem_pile.gems.copy()

    # Act: attempt the unaffordable purchase.
    result = board.buy_card(player, expensive_card)

    # Assert: the failure leaves every resource and card count unchanged.
    assert result == (False, "Cannot afford card")
    assert player.gems == starting_gems
    assert player.cards == starting_cards
    assert board.gem_pile.gems == starting_bank


def test_buy_board_card_replaces_field_card(board, player_with_resources, card):
    # Arrange: place an affordable card in the first level-one field slot.
    board.players[board.turn_player] = player_with_resources
    board.decks[0].field[0] = card

    # Act: buy the first card on level one.
    result = board.buy_board_card(level=1, row=1)

    # Assert: the purchase succeeds, the discount is added, and the field changes.
    assert result == (True, "")
    assert player_with_resources.cards[card.color] == 2
    assert board.decks[0].field[0] is not card


def test_buy_hand_card_removes_purchased_card(board, player_with_resources, card):
    # Arrange: give the current player an affordable card in hand.
    board.players[board.turn_player] = player_with_resources
    player_with_resources.hand.append(card)

    # Act: buy the first card in the player's hand.
    result = board.buy_hand_card(row=1)

    # Assert: the purchase succeeds and the card leaves the hand.
    assert result == (True, "")
    assert player_with_resources.cards[card.color] == 2
    assert player_with_resources.hand == []

# Reserving Cards


def test_reserve_board_card_awards_gold(board, card):
    # Arrange: put a known card in the first level-one field slot.
    current_player = board.players[board.turn_player]
    board.decks[0].field[0] = card
    starting_gold = board.gem_pile.gems["Au"]

    # Act: reserve the first card on level one.
    result = board.reserve_card(level=1, row=1)

    # Assert: the card enters the hand, the field is replaced, and gold transfers.
    assert result == (True, "")
    assert current_player.hand == [card]
    assert board.decks[0].field[0] is not card
    assert current_player.gems["Au"] == 1
    assert board.gem_pile.gems["Au"] == starting_gold - 1


def test_reserve_top_deck_card(board):
    # Arrange: record the card that will be popped from the level-one deck.
    current_player = board.players[board.turn_player]
    deck = board.decks[0]
    top_card = deck.cards[-1]
    starting_deck_size = len(deck.cards)

    # Act: reserve the top card by using row zero.
    result = board.reserve_card(level=1, row=0)

    # Assert: the top card moves to the hand and leaves the deck.
    assert result == (True, "")
    assert current_player.hand == [top_card]
    assert len(deck.cards) == starting_deck_size - 1


def test_reserve_card_fails_when_hand_is_full(board, card):
    # Arrange: fill the current player's hand to the three-card limit.
    current_player = board.players[board.turn_player]
    current_player.hand.extend([card, card, card])
    starting_gold = board.gem_pile.gems["Au"]

    # Act: attempt to reserve another board card.
    result = board.reserve_card(level=1, row=1)

    # Assert: the reservation fails before changing the hand or gold.
    assert result == (False, "You already have 3 cards in hand")
    assert len(current_player.hand) == 3
    assert board.gem_pile.gems["Au"] == starting_gold


def test_reserve_card_fails_for_empty_board_slot(board):
    # Arrange: remove the card from the requested field slot.
    current_player = board.players[board.turn_player]
    board.decks[0].field[0] = None

    # Act: attempt to reserve the empty slot.
    result = board.reserve_card(level=1, row=1)

    # Assert: the action reports the empty slot and leaves the hand empty.
    assert result == (False, "There is no card there")
    assert current_player.hand == []
