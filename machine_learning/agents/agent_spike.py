"""This is the Spike agent, which trains a Q-Network to play the game.
Spike plays to win, he doesn't care about anything other than maximizing his own winrate
Here are his goal stats when fighting against timmies:
winrate 2p: 60%
winrate 3p: 50%
winrate 4p: 40%
"""

import datetime
import os
from pathlib import Path

import matplotlib.pyplot as plt

from machine_learning.agents.agent import Agent
from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game


class Spike(Agent):
    """An agent that trains the model called "Spike".
    """

    def train(self):
        """Create a Spike model and train it by 
        having it play against random bots."""
        wins = 0
        draws = 0
        win_rates = []
        relative_wins = 0
        relative_draws = 0
        relative_turn_count = 0

        players = [Player("Spike", False),
                Player("Timmy #1", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #2", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #3", False, policy=QNetworkPolicy.from_file("timmy_model"))]

        game = Game(players)

        for i in range(self.total_games):
            if i % 500 == 0:
                print(f"Training game {i}: wins={wins}, draws={draws}, "
                    + f"relative_winrate: {relative_wins / (500 - relative_draws)}, "
                    + f"relative_turn_count: {relative_turn_count / 500}")
                relative_wins = 0
                relative_draws = 0
                relative_turn_count=0

            num_players = i % 3 + 2 # Cycles between 2, 3, and 4 players

            result = self.play_single_game(game, players[0:num_players])

            if result.name == 'Spike':
                wins += 1
                relative_wins += 1
            if result.name == 'Nobody':
                draws += 1
                relative_draws += 1

            self.n_games += 1
            relative_turn_count += game.board.turn_count
            self.train_long_memory()
            win_rates.append(wins / self.n_games)

        self.save_checkpoint("spike_model")

        print(f"Spike won {wins} out of {self.total_games} games.")
        print(f"Spike drew {draws} out of {self.total_games} games.")


    def evaluate_board(self, board, result, move_valid, prev_board_value):
        """Evaluate the current state of the board.
        
        Returns the evaluation of the board for the given player."""

        points = 0

        if not move_valid:
            return -20, prev_board_value # Points for invalid move

        if result is not None:
            if result.name == "Spike":
                return 400, prev_board_value # Points for victory
            if result.name == "Nobody":
                return 50, prev_board_value # Points for draw
            return -150, prev_board_value # Points for defeat

        #Model is always in the first position
        player = board.players[0]

        # For each gem you have, get 0.1 points for each card on the board that
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
        points += player.gems["Au"] * 1

        # Get 10 points for each card held
        points += (player.cards["W"] +
                    player.cards["U"] +
                    player.cards["B"] +
                    player.cards["R"] +
                    player.cards["G"]) * 10

        #Get 30 points For each score point the player has
        points += (player.points * 30)

        # Lose 1 point for the level of the card reserved
        # Spamming card reservations when you can't afford them later is penalized
        for card in player.hand:
            points -= card.level

        # Track the threat of the strongest opponent,
        # Punish Spike for having stronger opponents
        opponent_points = 0
        for opponent in board.players[1:]:
            opponent_threat = 0
            opponent_threat += (opponent.cards["W"] +
                                opponent.cards["U"] +
                                opponent.cards["B"] +
                                opponent.cards["R"] +
                                opponent.cards["G"]) * 3
            opponent_threat += (opponent.points * 15)

            # Only punish for the opponent that's the biggest threat
            opponent_points = max(opponent_points, opponent_threat)


        # Punish having opponents with more points and cards slightly
        points -= opponent_points

        # Return the net reward
        return (points - prev_board_value), points

    def evaluate_model(self):
        """Evaluate Spike's performance,
        model the win rate against 1 opponent,
        2 opponents, and 3 opponents."""

        _game_count = 1000

        # Get model player policy
        model = Player("Spike", False, QNetworkPolicy.from_file("spike_model"))

        timmy_policy = QNetworkPolicy.from_file("timmy_model")

        #2 player winrate
        print("Evaluating 2-player win rate...")
        winrate_2p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy)],
                                    _game_count)

        #3 player winrate
        print("Evaluating 3-player win rate...")
        winrate_3p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy)],
                                    _game_count)

        #4 player winrate
        print("Evaluating 4-player win rate...")
        winrate_4p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy),
                                    Player("Timmy #3", False, policy=timmy_policy)],
                                    _game_count)

        print(f"winrate 2p: {winrate_2p}")
        print(f"winrate 3p: {winrate_3p}")
        print(f"winrate 4p: {winrate_4p}")

        return (winrate_2p >= 0.6 and
            winrate_3p >= 0.5 and
            winrate_4p >= 0.4 )

    def evaluate_x_players(self, players: list[Player], _game_count: int = 1000):
        """Play _game_count games with the attached players and evaluate the win rate of Spike.
        Used to evaluate the model for a specific number of players."""

        wins = 0
        for _ in range(_game_count):
            game = Game(players)
            result = game.play()
            if result is not None and result.name == "Spike":
                wins += 1

            for player in players:
                player.reset()

        return wins / _game_count


if __name__ == "__main__":
    #Play 10000 training games, then 3000 evaluation games.
    #repeat until desired performance is achieved

    agent = Spike(total_games=10000)
    agent.load_checkpoint("spike_model")

    success = False

    agent.train()
    success = agent.evaluate_model()
    print(f"Evaluation success: {success}")
