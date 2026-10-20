from datetime import datetime
import os
from pathlib import Path

from matplotlib import pyplot as plt

from machine_learning.agents.agent import Agent
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game


class EvaluateTimmy(Agent):
    def __init__(self, total_games=1000):
        Agent.__init__(self, total_games=total_games)

    def evaluate(self, num_players: int):
        self.n_games = 0
        wins = 0
        draws = 0

        players = [Player("Timmy", False),
                Player("Random1", False),
                Player("Random2", False),
                Player("Random3", False)]

        game = Game(players)

        print(f"Evaluating {self.total_games} games with {num_players} players.")

        for _ in range(self.total_games):
            result = self.play_single_game(game, players[0:num_players])

            if result.name == 'Timmy':
                wins += 1
            if result.name == 'Nobody':
                draws += 1

            self.n_games += 1

        print("Evaluation complete.")
        print(f"Total games played: {self.n_games}")
        print(f"Timmy won {wins} out of {(self.total_games - draws)} games.")
        print(f"Timmy drew {draws} out of {(self.total_games - draws)} games.")
        print(f"Win Rate: {wins / (self.total_games - draws)}")
        return wins / (self.total_games - draws)

    def play_single_game(self, game: Game, players: list[Player]):
        """Play a single game and return the result."""
        result = game.training_game(players)

        while result is None:
            original_state = self.get_board_state(game.board)

            # Get moves in order of best to worst according to the model's evaluation
            moves = self.get_evaluation(original_state)
            moves_attempted = 0

            for move in moves:
                result, valid_move = game.take_agent_action(move)
                if valid_move:
                    break
                moves_attempted += 1

            if moves_attempted == len(moves):
                # Pass the turn after verifying there are no legal actions.
                result, valid_move = game.take_agent_action(None)

        return result

if __name__ == "__main__":
    evaluator = EvaluateTimmy()
    evaluator.model.load("timmy_model")
    evaluator.evaluate(2)
    evaluator.evaluate(3)
    evaluator.evaluate(4)
