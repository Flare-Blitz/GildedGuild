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
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game
from machine_learning.agents.model_evaluation.evaluate_timmy import EvaluateTimmy


class Timmy(Agent):
    """An agent that trains the model called "Timmy".
    Timmy is a simple model that learnd by playing against
    bots that take random actions."""

    def train(self):
        """Create a Timmy model and train it by 
        having it play against random bots."""
        wins = 0
        draws = 0
        win_rates = []

        players = [Player("Timmy", False),
                Player("Random1", False),
                Player("Random2", False),
                Player("Random3", False)]

        game = Game(players)

        for i in range(self.total_games):
            if i % 100 == 0:
                print(f"Training game {i}: wins={wins}, draws={draws}")
            num_players = i % 3 + 2 # Cycles between 2, 3, and 4 players

            result = self.play_single_game(game, players[0:num_players])

            if result.name == 'Timmy':
                wins += 1
            if result.name == 'Nobody':
                draws += 1

            self.n_games += 1
            self.train_long_memory()
            win_rates.append(wins / self.n_games)

        self.model.save("timmy_model")

        print(f"Timmy won {wins} out of {self.total_games} games.")
        print(f"Timmy drew {draws} out of {self.total_games} games.")

    def play_single_game(self, game: Game, players: list[Player]):
        """Play a single game and return the result."""
        result = game.training_game(players)

        while result is None:
            original_state = self.get_board_state(game.board)
            moves = self.get_training_actions(original_state)
            moves_attempted = 0

            for move in moves:
                result, valid_move = game.take_agent_action(move)

                # Create a one-hot encoded action vector to train the model
                action = [0] * 45
                action[move] = 1

                next_state = self.get_board_state(game.board)

                reward = self.evaluate_board(game.board, result, valid_move)

                done = result is not None

                self.train_short_memory(original_state, action, reward, next_state, done)
                self.remember(original_state, action, reward, next_state, done)

                if valid_move:
                    break
                moves_attempted += 1

            if moves_attempted == len(moves):
                # Pass the turn after verifying there are no legal actions.
                result, valid_move = game.take_agent_action(None)

        return result


    def evaluate_board(self, board, result, move_valid):
        """Evaluate the current state of the board.
        
        Returns the evaluation of the board for the given player."""

        points = 0

        if not move_valid:
            points -= 20 # Points for invalid move
        else:
            if result is not None:
                if result.name == "Timmy":
                    points += 100 # Points for victory
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
                        player.cards["G"])

            #Get 25 points For each score point the player has
            points += (player.points * 25)

            # Get 1 point for each card in hand
            points += len(player.hand)

        return points

if __name__ == "__main__":
    agent = Timmy(total_games=1000)
    agent.model.load("timmy_model")
    agent.train()

    #Evaluate Timmy's performance.
    print("Evaluating Timmy's performance...")
    evaluator = EvaluateTimmy()
    evaluator.model.load("timmy_model")
    WINRATE_2P = evaluator.evaluate(2)
    WINRATE_3P = evaluator.evaluate(3)
    WINRATE_4P = evaluator.evaluate(4)

    plt.bar(["2 Players", "3 Players", "4 Players"], [WINRATE_2P, WINRATE_3P, WINRATE_4P])
    plt.xlabel("Number of Players")
    plt.ylabel("Win Rate")
    plt.title("Timmy Win Rate vs Number of Players")
    plt.ylim(0, 1)
    folder_path = Path(__file__).parent / 'Graphs/Timmy'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = ("timmy_eval_graph" +
        datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +
        ".png")
    file_name = os.path.join(folder_path, file_name)

    plt.savefig(file_name)
    plt.show()
