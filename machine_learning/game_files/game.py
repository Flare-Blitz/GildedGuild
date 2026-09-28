"""
This module contains a gymnasium for simulating the game Gilded Guild.
It contains classes for every object used in the game, including cards, tiles, 
players, and the board itself.
"""
import random
from machine_learning.game_files.components import(
    ActionType,
    Action,
    Player,
    Board
)


class Game:
    """Represents the overall game, managing the game state.
    It takes and processes user actions"""
    def __init__(self, players: list[Player]):
        self.board = Board(players)
        self.all_actions = self._generate_all_actions()

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

    def _generate_all_actions(self):
        """Generates a list of all possible actions in the game."""
        actions = []
        colors = ("W", "U", "B", "R", "G")

        for color in colors:
            actions.append(Action(ActionType.TAKE_GEMS, colors=(color, color)))

        for i, color1 in enumerate(colors):
            for j, color2 in enumerate(colors[i + 1:], i + 1):
                for color3 in colors[j + 1:]:
                    actions.append(Action(ActionType.TAKE_GEMS, colors=(color1, color2, color3)))

        for level in range(1, 4):
            for row in range(1, 5):
                actions.append(Action(
                    ActionType.BUY_BOARD_CARD,
                    level=level,
                    row=row
                ))

        for row in range(1, 4):
            actions.append(Action(
                ActionType.BUY_HAND_CARD,
                row=row
            ))

        for level in range(1, 4):
            for row in range(0, 5):
                actions.append(Action(
                    ActionType.RESERVE_CARD,
                    level=level,
                    row=row
                ))

        return tuple(actions)


    def take_action(self):
        """
        This function takes an action from the current player.
        It can be either a human player or an ML Model.
        Currently only handles human players
        """
        # For now, we will assume all players are human
        if self.board.players[self.board.turn_player].is_human:
            self.take_human_action()
        else:
            self.take_random_action()

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
            success, message = self.process_action(user_input)

            if success is True:
                # The move was valid, return
                break

    def get_human_input(self) -> Action:
        """
        This function prompts the human player for input and returns an Action object.
        It handles different types of actions, including taking gems, 
        purchasing cards, and reserving cards.
        """
        print(f"{self.board.players[self.board.turn_player].name}'s Turn")
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

    def take_random_action(self):
        """Randomize the order of actions, then take the first valid one."""
        moves = random.sample(self.all_actions, len(self.all_actions))

        for move in moves:
            print(move)

        for move in moves:
            success, _ = self.process_action(move)
            if success:
                print(f"Bot {self.board.players[self.board.turn_player].name} took action: {move}")
                return

        # If there are NO valid actions, return without taking any action.
        print(f"Bot {self.board.players[self.board.turn_player].name} has no legal moves.")
        return

    def process_action(self, move: Action):
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
