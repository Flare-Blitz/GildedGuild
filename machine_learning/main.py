"""This is a file used for running the machine learning project. When being run,
It will start a game of Gilded Guild between 2 players."""

from machine_learning.game_files.game import Game

game = Game(2)

game.play()
