import math

import matplotlib.pyplot as plt

from machine_learning.agents.agent import Agent
from machine_learning.game_files.components import Player
from machine_learning.game_files.game import Game


class Timmy(Agent):
    """An agent that trains the model called "Timmy".
    Timmy is a simple model that learnd by playing against
    bots that take random actions."""

    def train(self):
        """Create a Timmy model and train it by 
        having it play against random bots."""

        num_games = 50000
        wins = 0
        draws = 0
        win_rates = []

        players = [Player("Timmy", False),
                Player("Random1", False),
                Player("Random2", False),
                Player("Random3", False)]

        game = Game(players)

        for i in range(num_games):
            if i % 100 == 0:
                print(f"Training game {i}: wins={wins}, draws={draws}")
            num_players = i % 3 + 2 # Cycles between 2, 3, and 4 players
            result, _ = game.training_game(players[0:num_players])

            while result is None:
                original_state = self.get_board_state(game.board)
                move = self.get_action(original_state)
                result, valid_move = game.take_agent_action(move)

                # Create a one-hot encoded action vector to train the model
                action = [0] * 45
                action[move] = 1

                next_state = self.get_board_state(game.board)

                done = result is not None

                reward = self.evaluateBoard(game.board, result, valid_move)
                self.train_short_memory(original_state, action, reward, next_state, done)
                self.remember(original_state, action, reward, next_state, done)

            if result.name == 'Timmy':
                wins += 1
            if result.name == 'Nobody':
                draws += 1

            self.n_games += 1
            win_rates.append(wins / self.n_games)

        self.model.save("timmy_model")

        print(f"Timmy won {wins} out of {num_games} games.")
        print(f"Timmy drew {draws} out of {num_games} games.")

        self.save_graph(win_rates, num_games)


    def evaluateBoard(self, board, result, move_valid):
        """Evaluate the current state of the board.
        
        Returns the evaluation of the board for the given player."""

        points = 0

        if not move_valid:
            points -= 200 # Points for invalid move
        elif result is not None:
            if result.name == "Timmy":
                points += 500 # Points for victory
            elif result.name == "Nobody":
                points -= 50 # Points for draw
            else:
                points -= 250 # Points for defeat
        else:
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

            #Get 15 points For each score point the player has
            points += (player.points * 15)

            # Get 1 point for each card in hand
            points += len(player.hand)

        k = 0.01

        points = points / math.exp(board.turn_count * k)
        return points

    def save_graph(self, win_rates, num_games):
        """Display the training results graph to the user.
        Then save it to a timmy folder"""
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, num_games + 1), win_rates, label="Win rate")
        plt.xlabel("Training game")
        plt.ylabel("Average win rate")
        plt.title("Timmy Average Win Rate During Training")
        plt.ylim(0, 1)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()

        folder_path = Path(__file__).parent / 'Graphs/Timmy'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_name = ("timmy_training_graph" +
            datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +
            ".png")
        file_name = os.path.join(folder_path, file_name)

        plt.savefig(file_name)
        plt.show()


if __name__ == "__main__":
    agent = Timmy()
    agent.model.load("timmy_model_v2.pth")
    agent.train()
