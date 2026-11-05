"""This is the Timmy agent, which trains a Q-Network to play the game.
Timmy plays games to have fun, so isn't as concerned with winning as with enjoying the process.
To reflect this, Timmy will be trained against opponents who only make random moves, creating a bot
that can play the game, but isn't very effictive at out performing other players.
Timmy is desgined to be the first bot, and other bots will be trained based off of Timmy."""

import datetime
import os
from pathlib import Path

import matplotlib.pyplot as plt

from machine_learning.agents.agent import Agent
from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game


class Timmy(Agent):
    """An agent that trains the model called "Timmy".
    Timmy is a simple model that learnd by playing against
    bots that take random actions."""

    def train(self):
        """Create a Timmy model and train it by 
        having it play against random bots."""
        wins = 0
        draws = 0
        relative_wins = 0
        relative_draws = 0

        players = [Player("Timmy", False),
                Player("Random1", False),
                Player("Random2", False),
                Player("Random3", False)]

        game = Game(players)

        for i in range(self.total_games):
            if i % 500 == 0:
                print(f"Training game {i}: wins={wins}, draws={draws}, "
                    + f"relative_winrate: {relative_wins / (500 - relative_draws)}, ")
                relative_wins = 0
                relative_draws = 0

            num_players = i % 3 + 2 # Cycles between 2, 3, and 4 players

            result = self.play_single_game(game, players[0:num_players])

            if result.name == 'Timmy':
                wins += 1
                relative_wins += 1
            if result.name == 'Nobody':
                draws += 1
                relative_draws += 1

            self.n_games += 1
            self.train_long_memory()

        self.save_checkpoint("timmy_model")

        print(f"Timmy won {wins} out of {self.total_games} games.")
        print(f"Timmy drew {draws} out of {self.total_games} games.")

    def evaluate_board(self, board, result, move_valid, prev_board_value):
        """Evaluate the current state of the board.
        
        Returns the evaluation of the board for the given player."""

        points = 0

        if not move_valid:
            points -= 20 # Points for invalid move
        else:
            if result is not None:
                if result.name == "Timmy":
                    points += 150 # Points for victory
                elif result.name == "Nobody":
                    points -= 20 # Points for draw
                else:
                    points -= 70 # Points for defeat
            player = board.players[0]

            # Get 1 point for each gem held
            points += (player.gems["W"] +
                player.gems["U"] +
                player.gems["B"] +
                player.gems["R"] +
                player.gems["G"] +
                player.gems["Au"])

            # Get 5 points for each card held
            points += (player.cards["W"] +
                        player.cards["U"] +
                        player.cards["B"] +
                        player.cards["R"] +
                        player.cards["G"]) * 5

            #Get 25 points For each score point the player has
            points += (player.points * 25)

            # Get 1 point for each card in hand
            points += len(player.hand)

        return points - prev_board_value, points

    def evaluate_model(self):
        """Evaluate Timmy's performance,
        model the win rate against 1 opponent,
        2 opponents, and 3 opponents."""

        _game_count = 1000

        # Get model player policy
        model = Player("Timmy", False, QNetworkPolicy.from_file("timmy_model"))

        #2 player winrate
        wins = 0
        for _ in range(_game_count):
            game = Game([model, Player("Opponent #1", False)])
            result = game.play()
            if result is not None and result.name == "Timmy":
                wins += 1
            model.reset()
        winrate_2p = wins / _game_count

        #3 player winrate
        wins = 0
        for _ in range(_game_count):
            game = Game([model,
                        Player("Opponent #1", False),
                        Player("Opponent #2", False)])
            result = game.play()
            if result is not None and result.name == "Timmy":
                wins += 1
            model.reset()
        winrate_3p = wins / _game_count

        #4 player winrate
        wins = 0
        for _ in range(_game_count):
            game = Game([model,
                        Player("Opponent #1", False),
                        Player("Opponent #2", False),
                        Player("Opponent #3", False)])
            result = game.play()
            if result is not None and result.name == "Timmy":
                wins += 1
            model.reset()
        winrate_4p = wins / _game_count

        print(f"winrate 2p: {winrate_2p}")
        print(f"winrate 3p: {winrate_3p}")
        print(f"winrate 4p: {winrate_4p}")

        return (winrate_2p >= 0.6
            and winrate_3p >= 0.4
            and winrate_4p >= 0.3)

if __name__ == "__main__":
    agent = Timmy(total_games=10000)
    agent.load_checkpoint("timmy_model")
    agent.train()

    #Evaluate Timmy's performance.
    agent.evaluate_model()
