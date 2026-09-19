"""This is a file used for running the machine learning project. When being run,
It will start a game of Gilded Guild between 2 players."""

from machine_learning.game_files.game import Game, Player

players = [Player(name="Arnold", is_human=True), Player(name="Benjamin", is_human=True)]
game = Game(players)

game.play()
