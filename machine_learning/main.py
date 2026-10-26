"""This is a file used for running the machine learning project. When being run,
It will start a game of Gilded Guild between 2 players."""

from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.game import Game, Player

players = [Player(
            name="Timmy A",
            is_human=False,
            policy=QNetworkPolicy.from_file("timmy_model")),
        Player(
            name="Timmy B",
            is_human=False,
            policy=QNetworkPolicy.from_file("timmy_model")),
        Player(
            name="Timmy C",
            is_human=False,
            policy=QNetworkPolicy.from_file("timmy_model")),
        # Player(
        #     name="Timmy D",
        #     is_human=False,
        #     policy=QNetworkPolicy.from_file("timmy_model")),
           ]

turn_counts = []
for i in range(100):
    game = Game(players)
    game.play()
    print(f"Game {i+1} finished. Turn Count: {game.board.turn_count}")
    turn_counts.append(game.board.turn_count)
    for player in players:
        player.reset()

print(f"Average Turn Count: {sum(turn_counts)/len(turn_counts) if turn_counts else 0}")
