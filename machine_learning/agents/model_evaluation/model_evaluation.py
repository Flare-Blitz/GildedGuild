"""This generates plot graphs for the overall evaluations of the model.
Here is a compiled list of graphs being generated:

- Winrate of timmy against 1, 2, and 3 random bots, with the target winrate
- Winrate of all 5 bots models against 1, 2, and 3 random bots.
- Winrate of all 5 bots against 1, 2, and 3 timmy bots
- Average turn count of games won, for Quentin and Steve against timmy bots
- Average turn count of games won, for all bots
- Average points earned on the final turn against timmy, for Johnny
- """

import os
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt

from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game

@dataclass
class ModelResults:
    """Stores the results of a model evaluation."""
    evaluation_label: str
    winrate: float
    drawrate: float
    avg_turn_count: float
    final_turn_points: float

class ModelEvaluation:
    """Creates plots for the overall evaluations of the models."""

    # A list of all models being trained, to be evaluea
    model_names = ["timmy_model", "quentin_model", "steve_model", "johnny_model", "spike_model"]
    # _game_count = 100

    def __init__(self, game_count: int = 5000):
        self.folder_path = Path(__file__).parent / 'Graphs'
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        self._game_count = game_count
        self.result_dictionary = {}

    def run(self):
        """Run the evaluation of all models and generate the plots."""
        self.result_dictionary = self.evaluate_all_models()

        self.generate_plots()

    def evaluate_all_models(self):
        """Evaluate all models by running a series of games
        Return a result dictionary that stores the evaluation results of each
        evaluation for each of the 5 models."""

        timmy_policy = QNetworkPolicy.from_file("timmy_model")
        result_dict = {}

        for model_name in self.model_names:
            result_dict[model_name] = {}
            model = Player(name=model_name,
                is_human=False,
                policy=QNetworkPolicy.from_file(model_name))
            result_dict[model_name]["2p_vs_random"] = self.evaluate_model([model,
                Player(name="random_bot", is_human=False)],
                "2p_vs_random")
            result_dict[model_name]["3p_vs_random"] = self.evaluate_model([model,
                Player(name="random_bot", is_human=False),
                Player(name="random_bot", is_human=False)],
                "3p_vs_random")
            result_dict[model_name]["4p_vs_random"] = self.evaluate_model([model,
                Player(name="random_bot", is_human=False),
                Player(name="random_bot", is_human=False),
                Player(name="random_bot", is_human=False)],
                "4p_vs_random")
            result_dict[model_name]["2p_vs_timmy"] = self.evaluate_model([model,
                Player(name="timmy_bot#1", is_human=False, policy=timmy_policy)],
                "2p_vs_timmy")
            result_dict[model_name]["3p_vs_timmy"] = self.evaluate_model([model,
                Player(name="timmy_bot#1", is_human=False, policy=timmy_policy),
                Player(name="timmy_bot#2", is_human=False, policy=timmy_policy)],
                "3p_vs_timmy")
            result_dict[model_name]["4p_vs_timmy"] = self.evaluate_model([model,
                Player(name="timmy_bot#1", is_human=False, policy=timmy_policy),
                Player(name="timmy_bot#2", is_human=False, policy=timmy_policy),
                Player(name="timmy_bot#3", is_human=False, policy=timmy_policy)],
                "4p_vs_timmy")
        return result_dict

    def evaluate_model(self, players: list[Player], evaluation_label: str) -> ModelResults:
        """Plays a bunch of games with the given player objects
        and reutrns the evaluation results of the first player bot
        Returns: winrate, drawrate, average turn count of wins,
        and points scored on the final turn of wins."""

        wins = 0
        draws = 0
        turns = 0
        final_turn_points = 0
        for _ in range(self._game_count):
            game = Game(players)
            result = game.play()
            if result is not None and result.name == players[0].name:
                wins += 1
                turns += game.board.turn_count
                final_turn_points += game.board.players[0].points_this_turn
            elif result is None:
                draws += 1

            for player in players:
                player.reset()

        return ModelResults(
            evaluation_label=evaluation_label,
            winrate=wins / self._game_count,
            drawrate=draws / self._game_count,
            avg_turn_count=turns / wins if wins > 0 else 0,
            final_turn_points=final_turn_points / wins if wins > 0 else 0
        )

    def generate_plots(self):
        """Generate plots based on the evaluation results stored in self.result_dictionary."""

        # Barchart of winrate of Timmy vs random bots
        self.generate_winrate_chart("Timmy vs Random Bots", ["Timmy"],
            [self.result_dictionary["timmy_model"]["2p_vs_random"].winrate],
            [self.result_dictionary["timmy_model"]["3p_vs_random"].winrate],
            [self.result_dictionary["timmy_model"]["4p_vs_random"].winrate])

        # Barchart of all models winrates vs bots
        two_p_winrates = []
        three_p_winrates = []
        four_p_winrates = []
        for _, result_list in self.result_dictionary.items():
            two_p_winrates.append(result_list["2p_vs_random"].winrate)
            three_p_winrates.append(result_list["3p_vs_random"].winrate)
            four_p_winrates.append(result_list["4p_vs_random"].winrate)

        self.generate_winrate_chart("All Models vs Random Bots", self.model_names,
            two_p_winrates, three_p_winrates, four_p_winrates)

        # Barchart of all models winrates vs timmy
        two_p_winrates = []
        three_p_winrates = []
        four_p_winrates = []
        for result_list in self.result_dictionary.values():
            two_p_winrates.append(result_list["2p_vs_timmy"].winrate)
            three_p_winrates.append(result_list["3p_vs_timmy"].winrate)
            four_p_winrates.append(result_list["4p_vs_timmy"].winrate)

        self.generate_winrate_chart("All Models vs Timmy", self.model_names,
            two_p_winrates, three_p_winrates, four_p_winrates)

        # Barchart of all models average win turn counts vs timmy
        two_p_turn_counts = []
        three_p_turn_counts = []
        four_p_turn_counts = []
        for result_list in self.result_dictionary.values():
            two_p_turn_counts.append(result_list["2p_vs_timmy"].avg_turn_count)
            three_p_turn_counts.append(result_list["3p_vs_timmy"].avg_turn_count)
            four_p_turn_counts.append(result_list["4p_vs_timmy"].avg_turn_count)

        self.generate_turn_count_chart(self.model_names,
            two_p_turn_counts, three_p_turn_counts, four_p_turn_counts)

        # Barchart of all models final turn points average vs timmy
        two_p_final_turn_points_avg = []
        three_p_final_turn_points_avg = []
        four_p_final_turn_points_avg = []
        for result_list in self.result_dictionary.values():
            two_p_final_turn_points_avg.append(result_list["2p_vs_timmy"].final_turn_points)
            three_p_final_turn_points_avg.append(result_list["3p_vs_timmy"].final_turn_points)
            four_p_final_turn_points_avg.append(result_list["4p_vs_timmy"].final_turn_points)

        self.generate_final_turn_points_avg_chart(self.model_names,
            two_p_final_turn_points_avg,
            three_p_final_turn_points_avg,
            four_p_final_turn_points_avg)

    def generate_winrate_chart(self,
        title,
        names: list[str],
        two_p_winrates: list[float],
        three_p_winrates: list[float],
        four_p_winrates: list[float]):
        """Generates a grouped barchart for winrate of the models against 2, 3, and 4 players."""
        winrates = {
            '2 Players': two_p_winrates,
            '3 Players': three_p_winrates,
            '4 Players': four_p_winrates
        }

        _, ax = plt.subplots(layout='constrained', figsize=(8, 6))

        res = ax.grouped_bar(winrates, tick_labels=names, group_spacing=1)
        for container in res.bar_containers:
            ax.bar_label(container, padding=3, fmt='%.2f')

        # Add some text for labels, title, etc.
        ax.set_ylabel('Winrate')
        ax.set_title(title)
        ax.legend(loc='lower center',
            bbox_to_anchor=(0.5, 1.02),
            ncol=3,
            frameon=False)
        ax.set_ylim(0, 1.1)

        plt.tight_layout()
        plt.savefig(os.path.join(self.folder_path, (title + ".png")))

    def generate_turn_count_chart(self,
        names: list[str],
        two_p_turn_counts: list[float],
        three_p_turn_counts: list[float],
        four_p_turn_counts: list[float]):
        """Generates a grouped barchart for turn count of the models against 2, 3, and 4 players."""
        turn_counts = {
            '2 Players': two_p_turn_counts,
            '3 Players': three_p_turn_counts,
            '4 Players': four_p_turn_counts,
        }

        _, ax = plt.subplots(layout='constrained', figsize=(8, 6))

        res = ax.grouped_bar(turn_counts, tick_labels=names, group_spacing=1)
        for container in res.bar_containers:
            ax.bar_label(container, padding=3, fmt='%.2f')

        # Add some text for labels, title, etc.
        ax.set_ylabel('Average Turn Count')
        ax.set_title("Average Turn Count for Win Vs. Timmy")
        ax.legend(loc='lower center',
                    bbox_to_anchor=(0.5, 1.02),
                    ncol=3,
                    frameon=False)
        ax.set_ylim(25, 40)

        plt.savefig(os.path.join(self.folder_path, "Average Turn Count vs. Timmy.png"))

    def generate_final_turn_points_avg_chart(self,
        names: list[str],
        two_p_final_turn_points_avg: list[float],
        three_p_final_turn_points_avg: list[float],
        four_p_final_turn_points_avg: list[float]):
        """Generates a grouped barchart for final turn points average
        of the models against 2, 3, and 4 players."""
        final_turn_points_avg = {
            '2 Players': two_p_final_turn_points_avg,
            '3 Players': three_p_final_turn_points_avg,
            '4 Players': four_p_final_turn_points_avg,
        }

        _, ax = plt.subplots(layout='constrained', figsize=(8, 6))

        res = ax.grouped_bar(final_turn_points_avg, tick_labels=names, group_spacing=1)
        for container in res.bar_containers:
            ax.bar_label(container, padding=3, fmt='%.2f')

        # Add some text for labels, title, etc.
        ax.set_ylabel('Final Turn Points Average')
        ax.set_title("Final Turn Points Average for Win Vs. Timmy")
        ax.legend(loc='lower center',
                    bbox_to_anchor=(0.5, 1.02),
                    ncol=3,
                    frameon=False)

        plt.savefig(os.path.join(self.folder_path, "Final Turn Points Average vs. Timmy.png"))


if __name__ == "__main__":
    evaluation = ModelEvaluation()
    evaluation.run()
