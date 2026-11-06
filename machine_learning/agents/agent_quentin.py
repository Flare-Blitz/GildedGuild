"""This is the Quentin agent, which trains a Q-Network to play the game.
Quentin is impatient, and will try to win as quickly as possible. He
will generally ignore his opponents, and focus entirely on winning in the
fewest number of turns. He is going to be taking risky plays, so we 
aren't counting the average turn count when he loses, only when he wins
The goal is 2 turns less than Timmy's average:
- Timmy 2p: ~35 turns, Quentin Target: ~33 turns
- Timmy 3p: ~30 turns, Quentin Target: ~28 turns
- Timmy 4p: ~28 turns, Quentin Target: ~26 turns
"""

from machine_learning.agents.agent import Agent
from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game


class Quentin(Agent):
    """An agent that trains the model called "Quentin".
    """

    def train(self):
        """Create a Quentin model and train it by 
        having it play against Timmy bots."""
        wins = 0
        draws = 0
        win_rates = []
        relative_wins = 0
        relative_draws = 0
        relative_turn_count = 0

        players = [Player("Quentin", False),
                Player("Timmy #1", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #2", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #3", False, policy=QNetworkPolicy.from_file("timmy_model"))]

        game = Game(players)

        for i in range(self.total_games):
            if i % 500 == 0:
                print(f"Training game {i}: wins={wins}, draws={draws}, "
                    + f"relative_winrate: {relative_wins / (500 - relative_draws)}, "
                    + f"relative_turn_count: {relative_turn_count / (relative_wins or 1)}")
                relative_wins = 0
                relative_draws = 0
                relative_turn_count=0

            num_players = i % 3 + 2 # Cycles between 2, 3, and 4 players

            result = self.play_single_game(game, players[0:num_players])

            if result.name == 'Quentin':
                wins += 1
                relative_wins += 1
                relative_turn_count += game.board.turn_count
            if result.name == 'Nobody':
                draws += 1
                relative_draws += 1

            self.n_games += 1
            self.train_long_memory()
            win_rates.append(wins / self.n_games)

        self.save_checkpoint("quentin_model")

        print(f"Quentin won {wins} out of {self.total_games} games.")
        print(f"Quentin drew {draws} out of {self.total_games} games.")


    def evaluate_board(self, board, result, move_valid, prev_board_value):
        """Evaluate the current state of the board.
        
        Returns the evaluation of the board for the given player."""

        points = 0

        if not move_valid:
            return -20, prev_board_value # Points for invalid move

        if result is not None:
            if result.name == "Quentin":
                return 300, prev_board_value # Points for victory
            if result.name == "Nobody":
                return 50, prev_board_value # Points for draw
            return -150, prev_board_value # Points for defeat

        #Model is always in the first position
        player = board.players[0]

        # For each gem you have, get 0.05 points for each card on the board that
        # matches that gem, for each matching gem on the card
        for deck in board.decks:
            for card in deck.field:
                if card is None:
                    continue
                points += 0.1 * player.gems["W"] * card.white
                points += 0.1 * player.gems["U"] * card.blue
                points += 0.1 * player.gems["B"] * card.black
                points += 0.1 * player.gems["R"] * card.red
                points += 0.1 * player.gems["G"] * card.green

        #Get flat 1 point per gold
        points += player.gems["Au"] * 0.5

        # Get 3 points for each card held
        points += (player.cards["W"] +
                    player.cards["U"] +
                    player.cards["B"] +
                    player.cards["R"] +
                    player.cards["G"]) * 6

        #Get 35 points For each score point the player has
        #Quentin needs points quickly, so greatly reward them
        points += (player.points * 35)

        # Return the net reward, with a slight punish to survival to incentivize aggressive play
        return (points - prev_board_value) - 2, points

    def evaluate_model(self):
        """Evaluate Quentin's performance,
        model the win rate against 1 opponent,
        2 opponents, and 3 opponents."""

        _game_count = 1000

        # Get model player policy
        model = Player("Quentin", False, QNetworkPolicy.from_file("Quentin_model"))

        timmy_policy = QNetworkPolicy.from_file("timmy_model")

        #2 player winrate
        print("Evaluating 2-player win rate...")
        winrate_2p, turnrate_2p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy)],
                                    _game_count)

        #3 player winrate
        print("Evaluating 3-player win rate...")
        winrate_3p, turnrate_3p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy)],
                                    _game_count)

        #4 player winrate
        print("Evaluating 4-player win rate...")
        winrate_4p, turnrate_4p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy),
                                    Player("Timmy #3", False, policy=timmy_policy)],
                                    _game_count)

        print(f"winrate 2p: {winrate_2p}, turnrate 2p: {turnrate_2p}")
        print(f"winrate 3p: {winrate_3p}, turnrate 3p: {turnrate_3p}")
        print(f"winrate 4p: {winrate_4p}, turnrate 4p: {turnrate_4p}")

        return (winrate_2p >= 0.6 and
            winrate_3p >= 0.4 and
            winrate_4p >= 0.3 and
            turnrate_2p <= 33 and
            turnrate_3p <= 28 and
            turnrate_4p <= 26)

    def evaluate_x_players(self, players: list[Player], _game_count: int = 1000):
        """Play _game_count games with the attached players and evaluate the win rate and 
        turn count averageof Quentin.
        Used to evaluate the model for a specific number of players."""

        wins = 0
        turns = 0
        for _ in range(_game_count):
            game = Game(players)
            result = game.play()
            if result is not None and result.name == "Quentin":
                wins += 1
                turns += game.board.turn_count

            for player in players:
                player.reset()

        return wins / _game_count, turns / wins


if __name__ == "__main__":
    #Play 10000 training games, then 3000 evaluation games.
    #repeat until desired performance is achieved

    agent = Quentin(total_games=10000)
    agent.load_checkpoint("quentin_model")

    success = False

    agent.train()
    success = agent.evaluate_model()
    print(f"Evaluation success: {success}")
