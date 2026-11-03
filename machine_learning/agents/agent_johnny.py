"""This is the Johnny agent, which trains a Q-Network to play the game.
Johnny loves a big flashy turn, so he gets rewarded for getting lots of points
on the final turn when he wins.
"""

import datetime
import os
from pathlib import Path

import matplotlib.pyplot as plt

from machine_learning.agents.agent import Agent
from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game


class Johnny(Agent):
    """An agent that trains the model called "Johnny".
    Johnny is a more complex algorithm that is designed to
    make big flashy turns, and win in the late game. It prioritizes
    high point gains on the final turn, meaning a good amount of
    setup for the final turn"""

    def train(self):
        """Create a Johnny model and train it by 
        having it play against Timmy bots."""
        wins = 0
        draws = 0
        win_rates = []
        relative_wins = 0
        relative_draws = 0
        relative_final_points = 0

        players = [Player("Johnny", False),
                Player("Timmy #1", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #2", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #3", False, policy=QNetworkPolicy.from_file("timmy_model"))]

        game = Game(players)

        for i in range(self.total_games):
            if i % 500 == 0:
                print(f"Training game {i}: wins={wins}, draws={draws}, "
                    + f"relative_winrate: {relative_wins / (500 - relative_draws)}, "
                    + f"relative_final_points_avg: {relative_final_points / (relative_wins or 1)}")
                relative_wins = 0
                relative_draws = 0
                relative_final_points=0

            num_players = i % 3 + 2 # Cycles between 2, 3, and 4 players

            result = self.play_single_game(game, players[0:num_players])

            if result.name == 'Johnny':
                wins += 1
                relative_wins += 1
                relative_final_points += players[0].points_this_turn
            if result.name == 'Nobody':
                draws += 1
                relative_draws += 1

            self.n_games += 1
            self.train_long_memory()
            win_rates.append(wins / self.n_games)

        self.save_checkpoint("johnny_model")

        print(f"Johnny won {wins} out of {self.total_games} games.")
        print(f"Johnny drew {draws} out of {self.total_games} games.")


    def evaluate_board(self, board, result, move_valid, prev_board_value):
        """Evaluate the current state of the board. prev_board_value stores
        the number of points Johnny had last turn, making him hyper focused
        on earning a lot of points in a single turn
        
        Returns the evaluation of the board for the given player."""

        points = 0

        if not move_valid:
            return -20, prev_board_value # Points for invalid move

        #Model is always in the first position
        player = board.players[0]

        if result is not None:
            if result.name == "Johnny":
                #Return number of points earned THIS TURN times 15 squared
                return (player.points_this_turn * 15) ** 2, prev_board_value # Points for victory
            if result.name == "Nobody":
                return -10, prev_board_value # Points for draw
            return -50, prev_board_value # Points for defeat

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

        # Get 20 points for each point earned
        points = player.points_this_turn * 20

        # Return the net reward, and scored points earned this turn
        return points - prev_board_value, points

    def evaluate_model(self):
        """Evaluate Johnny's performance,
        model the win rate against 1 opponent,
        2 opponents, and 3 opponents."""

        _game_count = 1000

        # Get model player policy
        model = Player("Johnny", False, QNetworkPolicy.from_file("johnny_model"))

        timmy_policy = QNetworkPolicy.from_file("timmy_model")

        #2 player winrate
        print("Evaluating 2-player win rate...")
        winrate_2p, final_turn_points_avg_2p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy)],
                                    _game_count)

        #3 player winrate
        print("Evaluating 3-player win rate...")
        winrate_3p, final_turn_points_avg_3p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy)],
                                    _game_count)

        #4 player winrate
        print("Evaluating 4-player win rate...")
        winrate_4p, final_turn_points_avg_4p = self.evaluate_x_players([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy),
                                    Player("Timmy #3", False, policy=timmy_policy)],
                                    _game_count)

        print(f"winrate 2p: {winrate_2p}, final_turn_points_avg 2p: {final_turn_points_avg_2p}")
        print(f"winrate 3p: {winrate_3p}, final_turn_points_avg 3p: {final_turn_points_avg_3p}")
        print(f"winrate 4p: {winrate_4p}, final_turn_points_avg 4p: {final_turn_points_avg_4p}")

        return (
            final_turn_points_avg_2p >= 4 and
            final_turn_points_avg_3p >= 4 and
            final_turn_points_avg_4p >= 4)

        # _, ax = plt.subplots(1, 2, figsize=(12, 6))

        # ax[0].bar(["2 Players", "3 Players", "4 Players"],
        #           [winrate_2p, winrate_3p, winrate_4p])

        # bars = ax[0].bar(["2 Players", "3 Players", "4 Players"],
        #                  [winrate_2p, winrate_3p, winrate_4p])
        # ax[0].bar_label(bars)
        # ax[0].set_xlabel("Number of Players")
        # ax[0].set_ylabel("Win Rate")
        # ax[0].set_title("Johnny Win Rate vs Number of Players")
        # ax[0].set_ylim(0, 1)

        # Turn rate plot
        # bars = ax[1].bar(["2 Players", "3 Players", "4 Players"],
        #                  [final_turn_points_avg_2p, final_turn_points_avg_3p, final_turn_points_avg_4p])
        # ax[1].bar_label(bars)
        # ax[1].set_xlabel("Number of Players")
        # ax[1].set_ylabel("Average Turn Count")
        # ax[1].set_title("Johnny Turn Count vs Number of Players")
        # ax[1].set_ylim(0, max(final_turn_points_avg_2p, final_turn_points_avg_3p, final_turn_points_avg_4p) * 1.1)
        # folder_path = Path(__file__).parent / 'Graphs/Johnny'
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)

        # file_name = ("johnny_eval_graph" +
        #     datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +
        #     ".png")
        # file_name = os.path.join(folder_path, file_name)

        # plt.savefig(file_name)
        # plt.show()

    def evaluate_x_players(self, players: list[Player], _game_count: int = 1000):
        """Play _game_count games with the attached players and evaluate the win rate and 
        turn count averageof Johnny.
        Used to evaluate the model for a specific number of players."""

        wins = 0
        final_turn_points = 0
        for _ in range(_game_count):
            game = Game(players)
            result = game.play()
            if result is not None and result.name == "Johnny":
                wins += 1
                final_turn_points += game.board.players[0].points_this_turn

            for player in players:
                player.reset()

        return wins / _game_count, final_turn_points / (wins or 1)


if __name__ == "__main__":
    #Play 10000 training games, then 3000 evaluation games.

    agent = Johnny(total_games=1)
    agent.load_checkpoint("johnny_model")

    success = False

    # agent.train()
    success = agent.evaluate_model()
    print(f"Evaluation success: {success}")
