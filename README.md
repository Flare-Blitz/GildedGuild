# GildedGuild
This is a repository housing the code for the GildedGuild Senior Design Project. When completed, it will allow users to run a react application that allows them to play a game programmed in unity against machine learning bots trained in a python gymnasium.

## Getting Started:

### Requirements
- Git

#### Frontend Requirements
- Node.js 20
- npm
- Docker

#### Machine Learning Python File Requirements
- Python 3.10 or 3.9

#### Gilded_Guild_Alpha Requrements
- Unity Hub
- Unity 6000.1.12f1

### Open React application
- docker compose up

### Run Python Game Simulation:
- python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest
python -m machine_learning.main

## Architecture Overview

The repository is organized into four areas: the frontend, backend, Unity code, and machine learning.

### Frontend

The frontend is a React application, using Next.js as a framework.

The frontend is a Next.js application using the App Router and TypeScript.

- Framework: Next.js 16 with React 19 and React DOM.
- Styling and tooling: Tailwind CSS 4 through the PostCSS plugin, ESLint 9, and TypeScript 5.
- structure: `frontend/app/` contains the root layout, page, global styles, and the placeholder API route directory.
- How it functions: Next.js serves the pages and handles the application runtime. `app/page.tsx` is currently the generated starter page, so the frontend does not yet render the game or call the backend/database.

### Database Backend

The database backend will store the necessary files required to initialize the database.
- .env.example: A environment file filled with dummy data
- test_SQL_Database.sql: an SQL file to create an initial database

### Gilded_Guild_Alpha

- All the Files that reside inside "Gilded_Guild_Alpha" come from the our Unity Demo from the Engineering Open House and have been improved upon since. Most of the Files are created by Unity and for the software to run Unity side. For now we can focus on the files we edit to make the game run.

- All of the files we have made edits to reside in the "Assets" Folder. Inside there are sub-folders that we use for orginization. 
Starting with the file "NGO_Minimal_Setup" this is for connecting multiple instances of the game together via Wi-Fi. Currently it is full of sample data, which we can apply once ready to the game.
Moving on to Scenes where the different screens come into play. Here is how we will be able to have a lobby which can connect people to a game, different from the actual game in order to keep screens organized.
- Next is the Scripts folder which houses all the coding we have done for the project. Here is currently some scripts to complete certain actions in the game.
- Afterwards is settings, however we haven't done anything with this folder as it is just for Unity's use.
- Lastly we have TextMesh Pro, which is a package offered by Unity for all UI text editing. Since this is a package that we use we haven't edited anything in here. 

### Machine Learning

The `machine_learning` directory contains 2 folders so far, game_files, and tests
- game_files contains the gymnasium that will be used to train the machine learning models. It doesn't support bot actions currently, but you can try out the gymnasium, where it simulates a 2 player game
- tests contains conftest.py, which stores a series of variables that can be used for testing the gynasium. It also contains game_test.py, which stores unit tests for the basic actions that a player is able to take.

#### Future Directories
- agents: This directory will contain a series of agents designed to train machine learning models. Each will have a different function to evaluate the models, resulting in multiple models with different playstlyes. They will be trained using Pytorch.
- models: This directory will hold the data for the models created by the agents.



Next is the Scripts folder which houses all the coding we have done for the project. Here is currently some scripts to complete certain actions in the game.
Afterwards is settings, however we haven't done anything with this folder as it is just for Unity's use.
Lastly we have TextMesh Pro, which is a package offered by Unity for all UI text editing. Since this is a package that we use we haven't edited anything in here. 


## Getting Started:

### Open React application
run:
docker compose up

### Run Python Game Simulation:
run:
cd MachineLearning
python3 main.py

