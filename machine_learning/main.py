"""This is a file used for running the machine learning project. When being run,
It will start a game of Gilded Guild between 2 players."""

from machine_learning.agents.ml_policy import QNetworkPolicy
from machine_learning.game_files.game import Game, Player

players = [Player(name="Average Andy", is_human=True),
           Player(
               name="Ben Bot",
               is_human=False,
               policy=QNetworkPolicy.from_file("timmy_model"),
           )]
game = Game(players)

game.play()
