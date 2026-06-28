import json
from dataclasses import dataclass
import random

@dataclass
class Card:
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
            "Black": "\033[95m", "Blue": "\033[94m", "Green": "\033[92m",
            "Red": "\033[91m", "White": "\033[97m", "Reset": "\033[0m"
        }
        color_symbol = (c.get(self.color, "") + "■" + c["Reset"]) if self.color else " "
        pts = str(self.points) if self.points > 0 else " "
        
        # Define fixed slots for costs to ensure consistent line length
        w = self._format_cost(self.white, "\033[97m", "W")
        u = self._format_cost(self.blue,  "\033[94m", "U")
        g = self._format_cost(self.green, "\033[92m", "G")
        r = self._format_cost(self.red,   "\033[91m", "R")
        b = self._format_cost(self.black, "\033[95m", "B")

        # Internal width is 9. 
        # Row 1 (W U G): 2+1+2+1+2 = 8. Need 1 more space.
        # Row 2 (R B): 2+1+2 = 5. Need 4 more spaces.

        return [
            f"┌──────────┐",
            f"│ {pts:<2}     {color_symbol} │",
            f"│          │",
            f"│ {w} {u} {b} │",
            f"│ {r} {g}    │",
            f"└──────────┘"
        ]


class Deck:
    def __init__(self, level):
        self.field = [None] * 4

        with open('MachineLearning/GameFiles/cards.json', 'r') as file:
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

        





@dataclass
class Tile:
    def __init__(self, points, white, blue, black, red, green):
        self.points = points
        self.white = white
        self.blue = blue
        self.black = black
        self.red = red
        self.green = green
    points: int = 0
    white: int = 0
    blue: int = 0
    black: int = 0
    red: int = 0
    green: int = 0

    def render(self):
        """Returns a list of strings representing the tile."""
        pts = str(self.points)
        costs = []
        if self.white: costs.append(f"\033[97m{self.white}\033[0m")
        if self.blue:  costs.append(f"\033[94m{self.blue}\033[0m")
        if self.black: costs.append(f"\033[95m{self.black}\033[0m")
        if self.red:   costs.append(f"\033[91m{self.red}\033[0m")
        if self.green: costs.append(f"\033[92m{self.green}\033[0m")
        
        # Calculate visible length to fix padding (ANSI codes are 0-width)
        visible_costs = [str(v) for v in [self.white, self.blue, self.green, self.red, self.black] if v > 0]
        actual_len = sum(len(s) for s in visible_costs) + (len(visible_costs) - 1 if visible_costs else 0)
        
        # Interior width is 7
        padding = max(0, 7 - actual_len)
        left_pad = " " * (padding // 2)
        right_pad = " " * (padding - (padding // 2))
        cost_line = f"{left_pad}{' '.join(costs)}{right_pad}"

        return [
            f"╔═════════╗",
            f"║  {pts.center(5)}  ║",
            f"║ {cost_line} ║",
            f"╚═════════╝"
        ]

class TileDeck:
    def __init__(self, cards):
        self.tiles = []
        with open('MachineLearning/GameFiles/tiles.json', 'r') as file:
            data = json.load(file)
            for i in range(cards):
                tileData = data.pop(random.randint(0, len(data) - 1))
                # Mapping logic if tiles.json uses uppercase keys
                normalized = {k.lower(): v for k, v in tileData.items()}
                self.tiles.append(Tile(**normalized))

    def render_row(self):
        rendered = [t.render() for t in self.tiles]
        return "\n".join("  ".join(row) for row in zip(*rendered))


class GemPile:
    def __init__(self, playerCount):
        # Map player count to gem counts to remove repetitive case logic
        counts = {2: 4, 3: 5, 4: 7}
        count = counts.get(playerCount, 7)
        
        self.white = self.blue = self.black = self.red = self.green = count
        self.gold = 5

    def __str__(self):
        return (f"Bank: \033[97m(W):{self.white}\033[0m  \033[94m(U):{self.blue}\033[0m  "
                f"\033[92m(G):{self.green}\033[0m  \033[91m(R):{self.red}\033[0m  "
                f"\033[95m(B):{self.black}\033[0m  \033[93m(Au):{self.gold}\033[0m")


class Board:
    def __init__(self, playerCount):
        self.level1Deck = Deck(1)
        self.level2Deck = Deck(2)
        self.level3Deck = Deck(3)

        self.playerCount = playerCount
        # Use list comprehension for dynamic player creation
        self.players = [Player() for _ in range(playerCount)]
        self.turnPlayer = random.randint(0, len(self.playerCount) - 1)

        self.tiles = TileDeck(playerCount + 1)
        self.gemPile = GemPile(playerCount)

        
    # This function displays the current board state
    # This is used when a player is playing
    def display(self):
        print("\n" + "="*65)
        print(" NOBLES ".center(65, "-"))
        print(self.tiles.render_row())
        
        print(" BOARD ".center(65, "-"))
        print(f"Level 3:\n{self.level3Deck.render_row()}")
        print(f"Level 2:\n{self.level2Deck.render_row()}")
        print(f"Level 1:\n{self.level1Deck.render_row()}")
        
        print(" BANK ".center(65, "-"))
        print(self.gemPile)
        
        print(" PLAYERS ".center(65, "-"))
        for i, p in enumerate(self.players):
            print(f"P{i+1}: {p.points}pts | Gems: W{p.whiteGems} U{p.blueGems} G{p.greenGems} R{p.redGems} K{p.blackGems} | "
                  f"Cards: W{p.whiteCards} U{p.blueCards} G{p.greenCards} R{p.redCards} K{p.blackCards}")
        print("="*65 + "\n")


class Player:
    def __init__(self):
        self.card1 = Card()
        self.card2 = Card()
        self.card3 = Card()
        self.points = 0
        self.whiteCards = 0
        self.blueCards = 0
        self.blackCards = 0
        self.redCards = 0
        self.greenCards = 0
        self.whiteGems = 0
        self.blueGems = 0
        self.blackGems = 0
        self.redGems = 0
        self.greenGems = 0
        self.gold = 0

#     def takeAction(self):
#         # TODO Replace this 
#         if True:


# class Game:
#     def __init__(self, playerCount):
#         self.board = Board(playerCount)

#     def play(self):
#         while True:
            