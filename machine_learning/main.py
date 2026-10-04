"""This is a file used for running the machine learning project. When being run,
It will start a game of Gilded Guild between 2 players."""

from machine_learning.game_files.game import Game, Player

players = [Player(name="Average Andy", is_human=True),
           Player(name="Ben Bot", is_human=False),
           Player(name="Carl Computer", is_human=False),
           Player(name="Digital Doug", is_human=False)]
game = Game(players)

game.play()
