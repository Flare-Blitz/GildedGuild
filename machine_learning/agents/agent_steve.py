"""This is the Timmy agent, which trains a Q-Network to play the game.
Steve is a degenerate, and tries to stall the game out before winning,
to accomplish this, I want him to ahve an overall positive winrate against timmy, and
end the game around 5 turns later than a game where every character is timmy
Here are some turn count estimates:
- Timmy 2p: ~35 turns, Steve Target: ~40 turns
- Timmy 3p: ~30 turns, Steve Target: ~35 turns
- Timmy 4p: ~28 turns, Steve Target: ~33 turns
"""

import datetime
import os
from pathlib import Path

import matplotlib.pyplot as plt

from machine_learning.agents.agent import Agent
from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game


class Steve(Agent):
    """An agent that trains the model called "Steve".
    Steve is a more complex algorithm that is designed to
    stall the game out, and win in the late game. It prioritizes
    long turn counts, and preventing the opponents from gaining
    stats"""

    def train(self):
        """Create a Steve model and train it by 
        having it play against random bots."""
        wins = 0
        draws = 0
        win_rates = []
        self.n_games = 0

        players = [Player("Steve", False),
                Player("Timmy #1", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #2", False, policy=QNetworkPolicy.from_file("timmy_model")),
                Player("Timmy #3", False, policy=QNetworkPolicy.from_file("timmy_model"))]

        game = Game(players)

        for i in range(self.total_games):
            if i % 100 == 0:
                print(f"Training game {i}: wins={wins}, draws={draws}")
            num_players = i % 3 + 2 # Cycles between 2, 3, and 4 players

            result = self.play_single_game(game, players[0:num_players])

            if result.name == 'Steve':
                wins += 1
            if result.name == 'Nobody':
                draws += 1

            self.n_games += 1
            self.train_long_memory()
            win_rates.append(wins / self.n_games)

        self.model.save("steve_model")

        # plt.plot(win_rates)
        # plt.xlabel("Games")
        # plt.ylabel("Win Rate")
        # plt.title("Steve Win Rate Over Time")
        # plt.show()

        print(f"Steve won {wins} out of {self.total_games} games.")
        print(f"Steve drew {draws} out of {self.total_games} games.")


    def evaluate_board(self, board, result, move_valid):
        """Evaluate the current state of the board.
        
        Returns the evaluation of the board for the given player."""

        points = 0

        if not move_valid:
            points -= 20 # Points for invalid move
        else:
            if result is not None:
                if result.name == "Steve":
                    points += 150 # Points for victory
                elif result.name == "Nobody":
                    points -= 10 # Points for draw
                else:
                    points -= 60 # Points for defeat
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
                        player.cards["G"])

            #Get 20 points For each score point the player has
            points += (player.points * 20)

            # Get 1 point for each card in hand
            points += len(player.hand)

            # Unlike timmy, reward long games by rewarding opponents
            # having fewer points and cards
            opponent_points = 0
            for opponent in board.players[1:]:
                opponent_points += (opponent.cards["W"] +
                                    opponent.cards["U"] +
                                    opponent.cards["B"] +
                                    opponent.cards["R"] +
                                    opponent.cards["G"]) / 2
                opponent_points += (opponent.points * 10)
                opponent_points += len(opponent.hand)

            # Punish having opponents with more points and cards slightly
            points -= opponent_points / len(board.players[1:])

            # Points increase as game progresses, starting with 1x,
            # Then increasing exponentially with 2x at turn 30, which
            # is the average game turn count, rewarding longer games
            k = 2 ** (board.turn_count / 30)

            if points > 0:
                points *= k
            else:
                points /= k

        return points

    def evaluate_model(self):
        """Evaluate Steve's performance,
        model the win rate against 1 opponent,
        2 opponents, and 3 opponents."""

        _game_count = 1000

        # Get model player policy
        model = Player("Steve", False, QNetworkPolicy.from_file("steve_model"))

        timmy_policy = QNetworkPolicy.from_file("timmy_model")

        #2 player winrate
        print("Evaluating 2-player win rate...")
        wins = 0
        turns = 0
        for _ in range(_game_count):
            game = Game([model, Player("Timmy #1", False, policy=timmy_policy)])
            result = game.play()
            turns += game.board.turn_count
            if result is not None and result.name == "Steve":
                wins += 1
            model.reset()
        winrate_2p = wins / _game_count
        turnrate_2p = turns / _game_count

        #3 player winrate
        print("Evaluating 3-player win rate...")
        wins = 0
        turns = 0
        for _ in range(_game_count):
            game = Game([model,
                        Player("Timmy #1", False, policy=timmy_policy),
                        Player("Timmy #2", False, policy=timmy_policy)])
            result = game.play()
            turns += game.board.turn_count
            if result is not None and result.name == "Steve":
                wins += 1
            model.reset()
        winrate_3p = wins / _game_count
        turnrate_3p = turns / _game_count

        #4 player winrate
        print("Evaluating 4-player win rate...")
        wins = 0
        turns = 0
        for _ in range(_game_count):
            game = Game([model,
                        Player("Timmy #1", False, policy=timmy_policy),
                        Player("Timmy #2", False, policy=timmy_policy),
                        Player("Timmy #3", False, policy=timmy_policy)])
            result = game.play()
            turns += game.board.turn_count
            if result is not None and result.name == "Steve":
                wins += 1
            model.reset()
        winrate_4p = wins / _game_count
        turnrate_4p = turns / _game_count

        return (winrate_2p >= 0.6 and
            winrate_3p >= 0.4 and
            winrate_4p >= 0.3 and
            turnrate_2p >= 40 and
            turnrate_3p >= 35 and
            turnrate_4p >= 33)

        # _, ax = plt.subplots(1, 2, figsize=(12, 6))

        # ax[0].bar(["2 Players", "3 Players", "4 Players"],
        #           [winrate_2p, winrate_3p, winrate_4p])

        # bars = ax[0].bar(["2 Players", "3 Players", "4 Players"],
        #                  [winrate_2p, winrate_3p, winrate_4p])
        # ax[0].bar_label(bars)
        # ax[0].set_xlabel("Number of Players")
        # ax[0].set_ylabel("Win Rate")
        # ax[0].set_title("Steve Win Rate vs Number of Players")
        # ax[0].set_ylim(0, 1)

        # Turn rate plot
        # bars = ax[1].bar(["2 Players", "3 Players", "4 Players"],
        #                  [turnrate_2p, turnrate_3p, turnrate_4p])
        # ax[1].bar_label(bars)
        # ax[1].set_xlabel("Number of Players")
        # ax[1].set_ylabel("Average Turn Count")
        # ax[1].set_title("Steve Turn Count vs Number of Players")
        # ax[1].set_ylim(0, max(turnrate_2p, turnrate_3p, turnrate_4p) * 1.1)
        # folder_path = Path(__file__).parent / 'Graphs/Steve'
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)

        # file_name = ("steve_eval_graph" +
        #     datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +
        #     ".png")
        # file_name = os.path.join(folder_path, file_name)

        # plt.savefig(file_name)
        # plt.show()


if __name__ == "__main__":
    #Play 10000 training games, then 3000 evaluation games.
    #repeat until desired performance is achieved

    agent = Steve(total_games=10000)
    agent.model.load("steve_model")

    success = False
    while not success:

        agent.train()

        success = agent.evaluate_model()

