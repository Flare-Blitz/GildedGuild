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
            f"┌──────────┐",
            f"│ {level_text:<2}  {pts:<2} {color_symbol} │",
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
    
    def replaceCard(self, spot):
        if len(self.cards) > 0:
            self.field[spot] = self.cards.pop()
        else:
            self.field[spot] = None

        





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

        self.gems = {
            "W" : count,
            "U" : count,
            "B" : count,
            "R" : count,
            "G" : count,
            "Au" : 5
        }

    def __str__(self):
        return (f"Bank: \033[97m(W):{self.gems["W"]}\033[0m  \033[94m(U):{self.gems["U"]}\033[0m  "
                f"\033[95m(B):{self.gems["B"]}\033[0m  \033[91m(R):{self.gems["R"]}\033[0m  "
                f"\033[92m(G):{self.gems["G"]}\033[0m  \033[93m(Au):{self.gems["Au"]}\033[0m")


class Board:
    def __init__(self, playerCount):
        self.decks = [Deck(1), Deck(2), Deck(3)]

        self.playerCount = playerCount
        # Use list comprehension for dynamic player creation
        self.players = [Player() for _ in range(playerCount)]
        self.turnPlayer = random.randint(0, self.playerCount - 1)

        self.tiles = TileDeck(playerCount + 1)
        self.gemPile = GemPile(playerCount)

        
    # This function displays the current board state
    # This is used when a player is playing
    def display(self):
        print("\n" + "="*65)
        print(" NOBLES ".center(65, "-"))
        print(self.tiles.render_row())
        
        print(" BOARD ".center(65, "-"))
        print(f"Level 3:\n{self.decks[2].render_row()}")
        print(f"Level 2:\n{self.decks[1].render_row()}")
        print(f"Level 1:\n{self.decks[0].render_row()}")
        
        print(" BANK ".center(65, "-"))
        print(self.gemPile)
        
        print(" PLAYERS ".center(65, "-"))
        for i, p in enumerate(self.players):
            print(
                f"P{i+1}: {p.points}pts | Gems: W:{p.gems['W']} U:{p.gems['U']} B:{p.gems['B']} R:{p.gems['R']} G:{p.gems['G']} Au:{p.gems['Au']} | "
                f"Cards: W:{p.cards['W']} U:{p.cards['U']} B:{p.cards['B']} R:{p.cards['R']} G:{p.cards['G']}"
            )
            if i != self.turnPlayer:
                print(f"  Hand levels: {p.render_hand()}")

        print(" CURRENT TURN HAND ".center(65, "-"))
        current_player = self.players[self.turnPlayer]
        hand_display = current_player.render_hand(is_current_player=True)
        for line in hand_display.splitlines():
            print(f"  {line}")

        print("="*65 + "\n")

    def advanceTurnPlayer(self):
        self.turnPlayer = (self.turnPlayer + 1) % self.playerCount

    # Check to see if the gem pile of that color has 4+ gems,
    # If there is, take 2 gems from that total and add it to the turn player's reserve
    # If there isn't, return a string outlining the error
    def take2Gems(self, gemColor):
        if self.gemPile.gems[gemColor] >= 4:
            #Transfer 2 gems from the gem pile to the turn player
            self.gemPile.gems[gemColor] -= 2
            self.players[self.turnPlayer].gems[gemColor] += 2
            return True, ""
        else:
            return False, "Selected pile has fewer than 4 gems"

    def take3Gems(self, gem1, gem2, gem3):
        if (self.gemPile.gems[gem1] > 0 
            and self.gemPile.gems[gem2] > 0 
            and self.gemPile.gems[gem3] > 0):

            self.gemPile.gems[gem1] -= 1
            self.gemPile.gems[gem2] -= 1
            self.gemPile.gems[gem3] -= 1

            self.players[self.turnPlayer].gems[gem1] += 1
            self.players[self.turnPlayer].gems[gem2] += 1
            self.players[self.turnPlayer].gems[gem3] += 1

            return True, ""
        else:
            return False, "Each selected pile must have at least one gem"
        
    def buyCard(self, player, card):
        whiteValue = player.cards["W"] + player.gems["W"]
        blueValue = player.cards["U"] + player.gems["U"]
        blackValue = player.cards["B"] + player.gems["B"]
        redValue = player.cards["R"] + player.gems["R"]
        greenValue = player.cards["G"] + player.gems["G"]

        #Calculates how short the player is to affording the card, to see if they have enough gold
        costDefecit = ( max(card.white - whiteValue, 0) +
            max(card.blue - blueValue, 0) +
            max(card.black - blackValue, 0) +
            max(card.red - redValue, 0) +
            max(card.green - greenValue, 0) )
        
        if costDefecit > player.gems["Au"]:
            return False, "Cannot afford card"
        
        #Get the cost that the player will pay
        whiteGemCost = min(card.white - player.cards["W"], player.gems["W"])
        blueGemCost = min(card.blue - player.cards["U"], player.gems["U"])
        blackGemCost = min(card.black - player.cards["B"], player.gems["B"])
        redGemCost = min(card.red - player.cards["R"], player.gems["R"])
        greenGemCost = min(card.green - player.cards["G"], player.gems["G"])
        goldCost = costDefecit

        #Add the gems back to the pile and subtract them from the player
        player.gems["W"] -= whiteGemCost
        self.gemPile.gems["W"] += whiteGemCost
        player.gems["U"] -= blueGemCost
        self.gemPile.gems["U"] += blueGemCost
        player.gems["B"] -= blackGemCost
        self.gemPile.gems["B"] += blackGemCost
        player.gems["R"] -= redGemCost
        self.gemPile.gems["R"] += redGemCost
        player.gems["G"] -= greenGemCost
        self.gemPile.gems["G"] += greenGemCost
        player.gems["Au"] -= goldCost
        self.gemPile.gems["Au"] += goldCost

        # Add the card to the player
        player.cards[card.color] += 1

        return True, ""
        
    def buyBoardCard(self, level, row):

        #level num MUST be 1, 2, or 3
        if level > 3 or level <= 0:
            return False, "Level must be 1, 2, or 3"
        #row num MUST be 1, 2, 3, or 4
        elif row > 4 or row <= 0:
            return False, "Row must be 1, 2, 3, or 4"
        
        card = self.decks[level-1].field[row-1]
        player = self.players[self.turnPlayer]

        if card == None:
            return False, "There is no card there"
        
        Success, message = self.buyCard(player, card)
        if(Success == False):
            return False, message

        # Replace the card with the next one in the deck
        self.decks[level - 1].replaceCard(row - 1)

        return True, ""
    
    def buyHandCard(self, row):

        player = self.players[self.turnPlayer]

        if row > len(player.hand) or row <= 0:
            return False, "Row must be 1, 2, or 3"
        
        card = player.hand[row-1]

        Success, message = self.buyCard(player, card)
        if(Success == False):
            return False, message
        
        player.hand.pop(row-1)
        return True, ""

    def reserveCard(self, level, row):
        
        player = self.players[self.turnPlayer]

        if len(player.hand) >= 3:
            return False, "You already have 3 cards in hand"


        #level num MUST be 1, 2, or 3
        if level > 3 or level <= 0:
            return False, "Level must be 1, 2, or 3"
        #row num MUST be 0, 1, 2, 3, or 4
        elif row > 4 or row < 0:
            return False, "Row must be 0, 1, 2, 3, or 4"

        #if row is 0, reserve the top card of the deck
        if row == 0:
            topCard = self.decks(level-1).cards.pop()
            if topCard == None:
                return False, "Deck is empty"
            
            player.hand.append(topCard)
        else:
            card = self.decks[level-1].field[row-1]
            if card == None:
                return False, "There is no card there"
            
            player.hand.append(card)
            self.decks[level - 1].replaceCard(row - 1)
        
        if self.gemPile.gems["Au"] > 0:
            player.gems["Au"] += 1
            self.gemPile.gems["Au"] -= 1

        return True, ""


class Player:
    def __init__(self):

        self.hand = []
        self.points = 0

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
        if not self.hand:
            return "(empty)"

        if is_current_player:
            rendered_cards = [card.render() for card in self.hand]
            card_width = max(len(line) for card in rendered_cards for line in card)
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
    def __init__(self, playerCount):
        self.board = Board(playerCount)
        self.play()

    def play(self):
        while True:
            # First, turn player takes an action
            self.takeAction()

            # Second, advance the turn player
            self.board.advanceTurnPlayer()

    def takeAction(self):
        # TODO Replace this with IsHuman when adding bots
        if True:
            self.takeHumanAction()
        else:
            self.takeBotAction()

    # Provides input for a human to take action
    def takeHumanAction(self):
        message = None
        while True:
            #1. Display the board so the human can see the current state
            self.board.display()

            #2. Check to see if their are any existing error messages
            if message != None:
                #Print error message
                print("ERROR: " + message)

            #2. Get their input at a string
            input = self.getHumanInput()

            #3. Process their input within the game
            success, message = self.processHumanAction(input)

            if success == True:
                # The move was valid, return
                break
            

    def getHumanInput(self):
        print(f"Player {self.board.turnPlayer + 1}'s Turn")
        print("Choose an action:")
        print("1. Take Gems (e.g., 'W U G' or 'RR')")
        print("2. Purchase Card on the board (e.g., 'P L1 2' for Level 1, Card 2)")
        print("3. Purchase Card in your hand (e.g., 'P H 2' for the 2nd card in your hand)")
        print("4. Reserve Card (e.g., 'E L2 1')")
        
        choice = input("> ").strip().upper().replace(" ", "")
        
        # This returns the raw input for processing by the game engine
        # Logic for validating and applying these moves will be handled in the game loop
        return choice
    
    # input: string move
    # This function takes a user action and r
    # return: string indicating if there is an error
    def processHumanAction(self, move):
        match move[0]:
            #If it starts with a color character, the user is taking gems
            case 'W' | 'U' | 'B' | 'R' | 'G' :
                match len(move):
                    case 2: #Taking 2 of the same gem
                        if move[0] == move[1]:
                            return self.board.take2Gems(move[0])
                        else:
                            return False, "Taking 2 gems must be the same color"
                    case 3: #Taking 3 different gems
                        if (move[0] != move[1]
                            and move[0] != move[2]
                            and move[1] != move[2]
                            and move[1] in {'W', 'U', 'B', 'R', 'G'}
                            and move[2] in {'W', 'U', 'B', 'R', 'G'}):
                            return self.board.take3Gems(move[0], move[1], move[2])
                        else:
                            return False, "When taking 3 gems, they must all be different"
                    case _:
                        return False, "Can only take 2 or 3 gems"
            #Purchasing a card
            case 'P':
                if len(move) == 4 and move[1] == 'L':
                    try:
                        #Get the level and row of the card
                        levelNum = int(move[2])
                        rowNum = int(move[3])

                        return self.board.buyBoardCard(levelNum, rowNum)
                    except ValueError:
                        return False, "Invalid purchase input, please put P -> L -> # #"
                elif len(move) == 3 and move[1] == 'H':
                    try:
                        #Get the row of the card in hand
                        rowNum = int(move[2])

                        return self.board.buyHandCard(rowNum)
                    except ValueError:
                        return False, "Invalid purchase input, please put P -> H -> #"
                else:
                    return False, "P must be followed by L or H"
            #Reserving a card
            case 'E':
                if len(move) == 4 and move[1] == 'L':
                    try:
                        #Get the level and row of the card
                        levelNum = int(move[2])
                        rowNum = int(move[3])

                        return self.board.reserveCard(levelNum, rowNum)
                    except ValueError:
                        return False, "Invalid reservation input, please put E -> L -> # #"
                else:
                    return False, "E must be followed by L, putting the level of the card"

            case _ :
                return False, "Unknown First Character"


            

