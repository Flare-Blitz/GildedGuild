# Developer Guide

## frontend
This contains the Node.js application. It will contain all frontend data, as well as any connections to the backend.

## Database Backend
This will contain the data to set up the mysql backend database

## machine_learning
This will contain all files necessary to create the machine learning bots
The bots will be housed in a models folder, exported as onyx files and 

## Gilded_Guild_Alpha
This contains the Unity build for the guiled guild game. All files needed to run the game in unity will be stored here.

## Workflows
- ci.yml: Contains linters for the application
- - ESLint: Javascript Linter
- - Pylint: Python Linter
- python-app.yml: Runs pytest unit testing
- secrets.yml: runs Trufflehog, to ensure no secrets are accidentally pushed. 

## .venv
Contains a virtual environment that will store all extensions needed to run the Machine Learning python files

## .gitignore
Any files that shouldn't be pushed should be present within the gitignore.

## pylintrc
A root file containing some additional rules to be followed by the Pylint linter.

## Using Pylint:
To use Pylint, install the pylint extension from the marketplace
Pylint will autmatically show formatting errors in files
To view more complex errors in a file, you can run ( pylint "fileDirectory" )

## Run Pytest locally
.venv/bin/python -m pytest MachineLearning/Tests
- This should be run from the root directory