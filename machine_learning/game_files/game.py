"""
This module contains a gymnasium for simulating the game Gilded Guild.
It contains classes for every object used in the game, including cards, tiles, 
players, and the board itself.
"""

from enum import Enum
import json
from dataclasses import dataclass
import random
from typing import Optional

@dataclass
class Cost:
    """Represents the cost of a tile in terms of different colored gems."""
    white: int = 0
    blue: int = 0
    black: int = 0
    red: int = 0
    green: int = 0

@dataclass
class Card:
    """Represents a card in the game."""

    level: int = 0
    color: str = ""
    points: int = 0
    white: int = 0
    blue: int = 0
    black: int = 0
    red: int = 0
    green: int = 0

    def _format_cost(self, val, color_code, char):
        return f"{color_code}{val}{char}\033[0m" if val > 0 else "  "

    def render(self):
        """Returns a list of strings representing the card visually."""
        c = {
            "B": "\033[95m", "U": "\033[94m", "G": "\033[92m",
            "R": "\033[91m", "W": "\033[97m", "Reset": "\033[0m"
        }
        level_text = f"L{self.level}" if self.level else " "
        color_symbol = (c.get(self.color, "") + "■" + c["Reset"]) if self.color else " "
        pts = str(self.points) if self.points > 0 else " "

        # Define fixed slots for costs to ensure consistent line length
        w = self._format_cost(self.white, "\033[97m", "W")
        u = self._format_cost(self.blue,  "\033[94m", "U")
        g = self._format_cost(self.green, "\033[92m", "G")
        r = self._format_cost(self.red,   "\033[91m", "R")
        b = self._format_cost(self.black, "\033[95m", "B")

        return [
            "┌──────────┐",
            f"│ {level_text:<2}  {pts:<2} {color_symbol} │",
            "│          │",
            f"│ {w} {u} {b} │",
            f"│ {r} {g}    │",
            "└──────────┘"
        ]


class Deck:
    """Represents a deck of cards for a specific level in the game."""

    def __init__(self, level):
        self.field = [None] * 4

        with open('machine_learning/game_files/cards.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            self.cards = []
            for card_data in data:
                # Normalize keys to lowercase to match dataclass
                normalized = {k.lower(): v for k, v in card_data.items()}
                if normalized.get('level') == level:
                    self.cards.append(Card(**normalized))

        random.shuffle(self.cards)
        for i in range(4):
            if self.cards:
                self.field[i] = self.cards.pop()

    def render_row(self):
        """Renders the 4 cards in the field side-by-side."""
        rendered_cards = [c.render() if c else ["           "] * 6 for c in self.field]
        # Combine lines of all cards horizontally
        combined = []
        for i in range(6):
            combined.append("  ".join(card[i] for card in rendered_cards))
        return "\n".join(combined)

    def replace_card(self, spot):
        """Replaces the card at the specified spot with a new card from the deck."""
        if len(self.cards) > 0:
            self.field[spot] = self.cards.pop()
        else:
            self.field[spot] = None

@dataclass
class Tile:
    """Defines a tile in the game, 
    which represents a noble with specific requirements and points."""

    points: int
    cost: Cost

    def render(self):
        """Returns a list of strings representing the tile."""
        pts = str(self.points)
        costs = []
        if self.cost.white:
            costs.append(f"\033[97m{self.cost.white}\033[0m")
        if self.cost.blue:
            costs.append(f"\033[94m{self.cost.blue}\033[0m")
        if self.cost.black:
            costs.append(f"\033[95m{self.cost.black}\033[0m")
        if self.cost.red:
            costs.append(f"\033[91m{self.cost.red}\033[0m")
        if self.cost.green:
            costs.append(f"\033[92m{self.cost.green}\033[0m")

        # Calculate visible length to fix padding (ANSI codes are 0-width)
        visible_costs = [
            str(v) for v in [
                self.cost.white,
                self.cost.blue,
                self.cost.green,
                self.cost.red,
                self.cost.black] if v > 0]

        actual_len = ( sum(len(s) for s in visible_costs) +
            (len(visible_costs) - 1 if visible_costs else 0) )

        # Interior width is 7
        padding = max(0, 7 - actual_len)
        left_pad = " " * (padding // 2)
        right_pad = " " * (padding - (padding // 2))
        cost_line = f"{left_pad}{' '.join(costs)}{right_pad}"

        return [
            "╔═════════╗",
            f"║  {pts.center(5)}  ║",
            f"║ {cost_line} ║",
            "╚═════════╝"
        ]

class TileDeck: # pylint: disable=too-few-public-methods
    """Represents the collection of noble tiles in the game."""

    def __init__(self, cards):
        self.tiles = []
        with open('machine_learning/game_files/tiles.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            for _ in range(cards):
                tile_data = data.pop(random.randint(0, len(data) - 1))
                # Mapping logic if tiles.json uses uppercase keys
                normalized = {k.lower(): v for k, v in tile_data.items()}
                cost = Cost(**{
                    color: normalized[color]
                    for color in ("white", "blue", "black", "red", "green")
                })
                self.tiles.append(Tile(points=normalized["points"], cost=cost))

    def render_row(self):
        """Renders the tiles side-by-side."""
        rendered = [t.render() for t in self.tiles]
        return "\n".join("  ".join(row) for row in zip(*rendered))


class GemPile: # pylint: disable=too-few-public-methods
    """Represents the pile of gems available in the game."""

    def __init__(self, player_count):
        # Map player count to gem counts to remove repetitive case logic
        counts = {2: 4, 3: 5, 4: 7}
        count = counts.get(player_count, 7)

        self.gems = {
            "W" : count,
            "U" : count,
            "B" : count,
            "R" : count,
            "G" : count,
            "Au" : 5
        }

    def __str__(self):
        return (f"Bank: \033[97m(W):{self.gems['W']}\033[0m  \033[94m(U):{self.gems['U']}\033[0m  "
                f"\033[95m(B):{self.gems['B']}\033[0m  \033[91m(R):{self.gems['R']}\033[0m  "
                f"\033[92m(G):{self.gems['G']}\033[0m  \033[93m(Au):{self.gems['Au']}\033[0m")


class Board:
    """Represents the game board, including decks, players, tiles, and gem piles.
    Also manages the game state, player turns, and actions."""

    def __init__(self, player_count):
        self.decks = [Deck(1), Deck(2), Deck(3)]

        self.player_count = player_count
        # Use list comprehension for dynamic player creation
        self.players = [Player() for _ in range(player_count)]
        self.starting_player = random.randint(0, self.player_count - 1)
        self.turn_player = self.starting_player

        for i, player in enumerate(self.players):
            player.name = f"Player {i + 1}"

        self.tiles = TileDeck(player_count + 1)
        self.gem_pile = GemPile(player_count)

    def display(self):
        """This function displays the current board state
        This is used when a player is playing"""

        print("\n" + "="*65)
        print(" NOBLES ".center(65, "-"))
        print(self.tiles.render_row())

        print(" BOARD ".center(65, "-"))
        print(f"Level 3:\n{self.decks[2].render_row()}")
        print(f"Level 2:\n{self.decks[1].render_row()}")
        print(f"Level 1:\n{self.decks[0].render_row()}")

        print(" BANK ".center(65, "-"))
        print(self.gem_pile)

        print(" PLAYERS ".center(65, "-"))
        for i, p in enumerate(self.players):
            print(
                f"P{i+1}: {p.points}pts"
                f" | Gems: W:{p.gems['W']} "
                f"U:{p.gems['U']} "
                f"B:{p.gems['B']} "
                f"R:{p.gems['R']} "
                f"G:{p.gems['G']} "
                f"Au:{p.gems['Au']} | "
                f"Cards: W:{p.cards['W']} "
                f"U:{p.cards['U']} "
                f"B:{p.cards['B']} "
                f"R:{p.cards['R']} "
                f"G:{p.cards['G']}"
            )
            if i != self.turn_player:
                print(f"  Hand levels: {p.render_hand()}")

        print(" CURRENT TURN HAND ".center(65, "-"))
        current_player = self.players[self.turn_player]
        hand_display = current_player.render_hand(is_current_player=True)
        for line in hand_display.splitlines():
            print(f"  {line}")

        print("="*65 + "\n")

    def advance_turn_player(self):
        """This function advances the turn to the next 
        player in a round-robin fashion."""
        self.turn_player = (self.turn_player + 1) % self.player_count

    def take_2_gems(self, gem_color):
        """ gem_color: str
            Check to see if the gem pile of that color has 4+ gems,
            If there is, take 2 gems from that total and add it to the turn player's reserve
            If there isn't, return a string outlining the error"""
        if self.gem_pile.gems[gem_color] >= 4:
            #Transfer 2 gems from the gem pile to the turn player
            self.gem_pile.gems[gem_color] -= 2
            self.players[self.turn_player].gems[gem_color] += 2
            return True, ""

        return False, "Selected pile has fewer than 4 gems"

    def take_3_gems(self, gem1, gem2, gem3):
        """ gem1, gem2, gem3: str
            Check to see if the gem piles of the specified colors have at least one gem each,
            If they do, take 1 gem from each and add it to the turn player's reserve
            If not, return a string outlining the error"""
        if (self.gem_pile.gems[gem1] > 0
            and self.gem_pile.gems[gem2] > 0
            and self.gem_pile.gems[gem3] > 0):

            self.gem_pile.gems[gem1] -= 1
            self.gem_pile.gems[gem2] -= 1
            self.gem_pile.gems[gem3] -= 1

            self.players[self.turn_player].gems[gem1] += 1
            self.players[self.turn_player].gems[gem2] += 1
            self.players[self.turn_player].gems[gem3] += 1

            return True, ""

        return False, "Each selected pile must have at least one gem"

    def buy_card(self, player, card):
        """
        player: Player
        card: Card
        This function checks if the player can afford the card, 
        and if they can, it deducts the appropriate gems and adds the card
        to the player's collection.
        """
        white_value = player.cards["W"] + player.gems["W"]
        blue_value = player.cards["U"] + player.gems["U"]
        black_value = player.cards["B"] + player.gems["B"]
        red_value = player.cards["R"] + player.gems["R"]
        green_value = player.cards["G"] + player.gems["G"]

        #Calculates how short the player is to affording the card, to see if they have enough gold
        cost_defecit = ( max(card.white - white_value, 0) +
            max(card.blue - blue_value, 0) +
            max(card.black - black_value, 0) +
            max(card.red - red_value, 0) +
            max(card.green - green_value, 0) )

        if cost_defecit > player.gems["Au"]:
            return False, "Cannot afford card"

        #Get the cost that the player will pay
        white_gem_cost = min(max(card.white - player.cards["W"], 0), player.gems["W"])
        blue_gem_cost = min(max(card.blue - player.cards["U"], 0), player.gems["U"])
        black_gem_cost = min(max(card.black - player.cards["B"], 0), player.gems["B"])
        red_gem_cost = min(max(card.red - player.cards["R"], 0), player.gems["R"])
        green_gem_cost = min(max(card.green - player.cards["G"], 0), player.gems["G"])
        gold_cost = cost_defecit

        #Add the gems back to the pile and subtract them from the player
        player.gems["W"] -= white_gem_cost
        self.gem_pile.gems["W"] += white_gem_cost
        player.gems["U"] -= blue_gem_cost
        self.gem_pile.gems["U"] += blue_gem_cost
        player.gems["B"] -= black_gem_cost
        self.gem_pile.gems["B"] += black_gem_cost
        player.gems["R"] -= red_gem_cost
        self.gem_pile.gems["R"] += red_gem_cost
        player.gems["G"] -= green_gem_cost
        self.gem_pile.gems["G"] += green_gem_cost
        player.gems["Au"] -= gold_cost
        self.gem_pile.gems["Au"] += gold_cost

        # Add the card to the player
        player.cards[card.color] += 1

        return True, ""

    def buy_board_card(self, level, row):
        """
        level: int
        row: int
        This function checks if the player can afford the card on the board,
        and if they can, it deducts the appropriate gems and adds the card
        to the player's collection. It also replaces the card on the board 
        with a new one from the deck.
        """

        #level num MUST be 1, 2, or 3
        if level > 3 or level <= 0:
            return False, "Level must be 1, 2, or 3"
        #row num MUST be 1, 2, 3, or 4
        if row > 4 or row <= 0:
            return False, "Row must be 1, 2, 3, or 4"

        card = self.decks[level-1].field[row-1]
        player = self.players[self.turn_player]

        if card is None:
            return False, "There is no card there"

        success, message = self.buy_card(player, card)
        if not success:
            return False, message

        # Replace the card with the next one in the deck
        self.decks[level - 1].replace_card(row - 1)

        return True, ""

    def buy_hand_card(self, row):
        """
        row: int
        This function checks if the player can afford the card in their hand,
        and if they can, it deducts the appropriate gems and adds the card
        to the player's collection. It also removes the card from the player's hand."""

        player = self.players[self.turn_player]

        if row > len(player.hand) or row <= 0:
            return False, "Row must be 1, 2, or 3"

        card = player.hand[row-1]

        success, message = self.buy_card(player, card)
        if not success:
            return False, message

        player.hand.pop(row-1)
        return True, ""

    def reserve_card(self, level, row):
        """
        level: int
        row: int
        This function allows the player to reserve a card from the board or the deck.
        The reserved card is added to the player's hand, and if possible, 
        the player also receives a gold gem from the gem pile.
        """

        player = self.players[self.turn_player]

        if len(player.hand) >= 3:
            return False, "You already have 3 cards in hand"


        #level num MUST be 1, 2, or 3
        if level > 3 or level <= 0:
            return False, "Level must be 1, 2, or 3"
        #row num MUST be 0, 1, 2, 3, or 4
        if row > 4 or row < 0:
            return False, "Row must be 0, 1, 2, 3, or 4"

        #if row is 0, reserve the top card of the deck
        if row == 0:
            deck = self.decks[level-1]
            if not deck.cards:
                return False, "Deck is empty"

            top_card = deck.cards.pop()
            player.hand.append(top_card)
        else:
            card = self.decks[level-1].field[row-1]
            if card is None:
                return False, "There is no card there"

            player.hand.append(card)
            self.decks[level - 1].replace_card(row - 1)

        if self.gem_pile.gems["Au"] > 0:
            player.gems["Au"] += 1
            self.gem_pile.gems["Au"] -= 1

        return True, ""

    def check_nobles(self):
        """
        This function checks if the current player meets the requirements to claim a noble tile.
        If they do, the tile is added to their collection and removed from the board."""

        player = self.players[self.turn_player]
        for tile in self.tiles.tiles:
            if (player.cards["W"] >= tile.cost.white and
                player.cards["U"] >= tile.cost.blue and
                player.cards["B"] >= tile.cost.black and
                player.cards["R"] >= tile.cost.red and
                player.cards["G"] >= tile.cost.green):

                player.points += tile.points
                player.tiles.append(tile)
                self.tiles.tiles.remove(tile)

                break  # Assuming a player can claim only one noble per turn

    def check_victory(self):
        """
        This function checks to see if a player has won by reaching 15 points or more.
        It only checks at the end of each turn cycle. 
        Returns the winning player if there is one, otherwise returns None.
        """
        if self.turn_player == self.starting_player:
            max_points = 0
            winner = None
            for player in self.players:
                if player.points >= 15 and player.points > max_points:
                    winner = player
                    max_points = player.points

            return winner

        return None

class ActionType(Enum):
    """Defines the types of actions a player can take in the game."""

    TAKE_GEMS = "take_gems"
    BUY_BOARD_CARD = "buy_board_card"
    BUY_HAND_CARD = "buy_hand_card"
    RESERVE_CARD = "reserve_card"

@dataclass(frozen=True)
class Action:
    """Represents an action taken by a player in the game."""
    action_type: ActionType
    colors: tuple[str, ...] = ()
    level: Optional[int] = None
    row: Optional[int] = None

class Player: # pylint: disable=too-few-public-methods
    """
    Represents a player in the game, 
    including their name, hand, points, tiles, gems, and cards.
    """

    def __init__(self):

        self.name = ""

        self.hand = []
        self.points = 0
        self.tiles = []

        self.gems = {
            "W" : 0,
            "U" : 0,
            "B" : 0,
            "R" : 0,
            "G" : 0,
            "Au" : 0
        }

        self.cards = {
            "W" : 0,
            "U" : 0,
            "B" : 0,
            "R" : 0,
            "G" : 0
        }

    def render_hand(self, is_current_player=False):
        """Renders the player's hand of cards.
        If is_current_player is True, it renders the full card details.
        Otherwise, it only shows the levels of the cards in hand."""

        if not self.hand:
            return "(empty)"

        if is_current_player:
            rendered_cards = [card.render() for card in self.hand]
            card_width = 12
            padded_cards = [
                [line.ljust(card_width) for line in card]
                for card in rendered_cards
            ]

            return "\n".join(
                "  ".join(card_lines[i] for card_lines in padded_cards)
                for i in range(6)
            )

        return "[" + ", ".join(f"L{card.level}" for card in self.hand) + "]"


class Game:
    """Represents the overall game, managing the game state.
    It takes and processes user actions"""
    def __init__(self, player_count):
        self.board = Board(player_count)

    def play(self):
        """
        This function runs the main game loop, alternating turns between players
        until a player wins. It handles action-taking and victory checking.
        """
        while True:
            # First, turn player takes an action
            self.take_action()

            self.board.check_nobles()

            winner = self.board.check_victory()
            if winner:
                print(f"Player {winner.name} has won the game!")
                break

            # Second, advance the turn player
            self.board.advance_turn_player()

    def take_action(self):
        """
        This function takes an action from the current player.
        It can be either a human player or an AI agent.
        Currently only handles human players
        """
        # For now, we will assume all players are human
        self.take_human_action()

    # Provides input for a human to take action
    def take_human_action(self):
        """
        This function handles the action-taking process for a human player.
        It displays the board, prompts for input, and processes the action.
        If the action is invalid, it displays an error message and prompts again."""
        message = None
        while True:
            #1. Display the board so the human can see the current state
            self.board.display()

            #2. Check to see if their are any existing error messages
            if message is not None:
                #Print error message
                print("ERROR: " + message)

            #2. Get their input at a string
            user_input = self.get_human_input()

            #3. Process their input within the game
            success, message = self.process_human_action(user_input)

            if success is True:
                # The move was valid, return
                break

    def get_human_input(self) -> Action:
        """
        This function prompts the human player for input and returns an Action object.
        It handles different types of actions, including taking gems, 
        purchasing cards, and reserving cards.
        """
        print(f"Player {self.board.turn_player + 1}'s Turn")
        print("Choose an action:")
        print("1. Take Gems (e.g., 'W U G' or 'RR')")
        print("2. Purchase Card on the board (e.g., 'P L1 2' for Level 1, Card 2)")
        print("3. Purchase Card in your hand (e.g., 'P H 2' for the 2nd card in your hand)")
        print("4. Reserve Card (e.g., 'E L2 1')")

        choice = input("> ").strip().upper().replace(" ", "")

        if (choice.startswith('W') or
            choice.startswith('U') or
            choice.startswith('B') or
            choice.startswith('R') or
            choice.startswith('G')):
            return Action(action_type=ActionType.TAKE_GEMS, colors=tuple(choice))
        if choice.startswith('P'):
            if len(choice) == 4 and choice[1] == 'L':
                try:
                    level = int(choice[2])
                    row = int(choice[3])
                    return Action(action_type=ActionType.BUY_BOARD_CARD, level=level, row=row)
                except ValueError:
                    print("Invalid input for board card purchase. Please use 'P L# #' format.")
            elif len(choice) == 3 and choice[1] == 'H':
                try:
                    row = int(choice[2])
                    return Action(action_type=ActionType.BUY_HAND_CARD, row=row)
                except ValueError:
                    print("Invalid input for hand card purchase. Please use 'P H #' format.")
        if choice.startswith('E'):
            if len(choice) == 4 and choice[1] == 'L':
                try:
                    level = int(choice[2])
                    row = int(choice[3])
                    return Action(action_type=ActionType.RESERVE_CARD, level=level, row=row)
                except ValueError:
                    print("Invalid input for reserving a card. Please use 'E L# #' format.")
        else:
            print("Invalid action. Please try again.")

        return None

    def process_human_action(self, move: Action):
        """
        move: Action
        This function processes the human player's action based on their input.
        It validates the action and executes it on the game board.
        Returns a tuple (success: bool, message: str) indicating whether the action was successful
        and any error message if applicable."""
        if not move:
            return False, "Action cannot be empty"

        handlers = {
            ActionType.TAKE_GEMS: self._process_take_gems,
            ActionType.BUY_BOARD_CARD: self._process_buy_board_card,
            ActionType.BUY_HAND_CARD: self._process_buy_hand_card,
            ActionType.RESERVE_CARD: self._process_reserve_card,
        }
        handler = handlers.get(move.action_type)
        if handler is None:
            return False, "Unknown action type"
        return handler(move)

    def _process_take_gems(self, move: Action):
        """Validate and execute a gem-taking action."""
        if len(move.colors) == 2:
            if move.colors[0] == move.colors[1]:
                return self.board.take_2_gems(move.colors[0])
            return False, "Taking 2 gems must be the same color"

        if len(move.colors) == 3:
            valid_colors = all(color in {'W', 'U', 'B', 'R', 'G'}
                               for color in move.colors)
            if len(set(move.colors)) == 3 and valid_colors:
                return self.board.take_3_gems(*move.colors)
            return False, "When taking 3 gems, they must all be different"

        return False, "Can only take 2 or 3 gems"

    def _process_buy_board_card(self, move: Action):
        """Validate and execute a board-card purchase."""
        if move.level is None or move.row is None:
            return False, "Level and row must be specified for buying a board card"
        return self.board.buy_board_card(move.level, move.row)

    def _process_buy_hand_card(self, move: Action):
        """Validate and execute a hand-card purchase."""
        if move.row is None:
            return False, "Row must be specified for buying a hand card"
        return self.board.buy_hand_card(move.row)

    def _process_reserve_card(self, move: Action):
        """Validate and execute a card reservation."""
        if move.level is None or move.row is None:
            return False, "Level and row must be specified for reserving a card"
        return self.board.reserve_card(move.level, move.row)



    def execute_action(self, action: Action):
        """
        action: Action
        This function executes the given action on the game board.
        It validates the action type and parameters, and calls the appropriate method on the board.
        Returns a tuple (success: bool, message: str) indicating whether the action was successful
        and any error message if applicable.
        """

        error = "Unknown action type"

        if action.action_type == ActionType.TAKE_GEMS:
            if len(action.colors) == 2 and action.colors[0] == action.colors[1]:
                return self.board.take_2_gems(action.colors[0])
            if len(action.colors) == 3 and len(set(action.colors)) == 3:
                return self.board.take_3_gems(*action.colors)
            error = "Invalid gem selection"
        elif action.action_type == ActionType.BUY_BOARD_CARD:
            if action.level is not None and action.row is not None:
                return self.board.buy_board_card(action.level, action.row)
            error = "Level and row must be specified for buying a board card"
        elif action.action_type == ActionType.BUY_HAND_CARD:
            if action.row is not None:
                return self.board.buy_hand_card(action.row)
            error = "Row must be specified for buying a hand card"
        elif action.action_type == ActionType.RESERVE_CARD:
            if action.level is not None and action.row is not None:
                return self.board.reserve_card(action.level, action.row)
            error = "Level and row must be specified for reserving a card"

        return False, error
