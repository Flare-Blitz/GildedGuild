"""This is the Johnny agent, which trains a Q-Network to play the game.
Johnny loves a big flashy turn, so he gets rewarded for getting lots of points
on the final turn when he wins.
"""

from machine_learning.agents.agent import Agent
from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.agents.model_evaluation.model_evaluation import ModelEvaluation
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
                return -5, prev_board_value # Points for draw
            return -75, prev_board_value # Points for defeat

        points += (player.gems["W"] +
                        player.gems["U"] +
                        player.gems["B"] +
                        player.gems["R"] +
                        player.gems["G"] +
                        player.gems["Au"])

        # Get 5 points for each card bought
        points += (player.cards["W"] +
                    player.cards["U"] +
                    player.cards["B"] +
                    player.cards["R"] +
                    player.cards["G"]) * 5

        # Get 15 points for each point earned
        points += player.points * 20

        # Return the net reward, and scored points earned this turn
        return points - prev_board_value, points

    def evaluate_model(self):
        """Evaluate Johnny's performance,
        model the win rate against 1 opponent,
        2 opponents, and 3 opponents."""

        _game_count = 3000

        # Get model player policy
        model = Player("Johnny", False, QNetworkPolicy.from_file("johnny_model"))

        timmy_policy = QNetworkPolicy.from_file("timmy_model")

        model_evaluator = ModelEvaluation(_game_count)

        #2 player winrate
        print("Evaluating 2-player win rate...")
        results_2p = model_evaluator.evaluate_model([model,
                                    Player("Timmy #1", False, policy=timmy_policy)],
                                    "Johnny vs 1 Timmy")

        #3 player winrate
        print("Evaluating 3-player win rate...")
        results_3p = model_evaluator.evaluate_model([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy)],
                                    "Johnny vs 2 Timmys")

        #4 player winrate
        print("Evaluating 4-player win rate...")
        results_4p = model_evaluator.evaluate_model([model,
                                    Player("Timmy #1", False, policy=timmy_policy),
                                    Player("Timmy #2", False, policy=timmy_policy),
                                    Player("Timmy #3", False, policy=timmy_policy)],
                                    "Johnny vs 3 Timmys")

        print(f"winrate 2p: {results_2p.winrate}, " +
            f"final_turn_points_avg 2p: {results_2p.final_turn_points}")
        print(f"winrate 3p: {results_3p.winrate}, " +
            f"final_turn_points_avg 3p: {results_3p.final_turn_points}")
        print(f"winrate 4p: {results_4p.winrate}, " +
            f"final_turn_points_avg 4p: {results_4p.final_turn_points}")

        return (
            results_2p.final_turn_points >= 4 and
            results_3p.final_turn_points >= 4 and
            results_4p.final_turn_points >= 4 and
            results_2p.winrate >= 0.4 and
            results_3p.winrate >= 0.3 and
            results_4p.winrate >= 0.2
            )


if __name__ == "__main__":
    #Play 10000 training games, then 9000 evaluation games.

    agent = Johnny(total_games=10000)
    agent.load_checkpoint("johnny_model")

    success = False

    while not success:
        agent.train()
        success = agent.evaluate_model()
        print(f"Evaluation success: {success}")
