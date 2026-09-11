# GildedGuild
This is a repository housing the code for the GildedGuild Senior Design Project. When completed, it will allow users to run a react application that allows them to play a game programmed in unity against machine learning bots trained in a python gymnasium.

## Getting Started:

### Requirements
- Git
- Docker
- Docker Compose

#### Frontend Requirements
- Node.js 20
- npm

#### Machine Learning Python File Requirements
- Python 3.10 or 3.9

#### Gilded_Guild_Alpha Requrements
- Unity Hub
- Unity 6000.1.12f1

### Open the Frontend and MySQL Database

The frontend runs in Next.js and connects to a MySQL database through a
server-side API route. Docker Compose starts both services.

#### Environment Setup

Create a root `.env` file beside `docker-compose.yml`:

```env
MYSQL_ROOT_PASSWORD=your_mysql_password
```

Create the frontend environment file from the committed template:

```bash
cp frontend/.env.example frontend/.env.local
```

Verify `frontend/.env.local` contains:

```env
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=mydb
DB_PORT=3306
```

The two password values must match. Do not commit either `.env` or
`frontend/.env.local`.

#### SQL Database Initialization

The file `Database Backend/test_SQL_Database.sql` creates the `mydb` database,
creates the `users` table, and inserts sample users using MySQL-compatible
`SHA2` hashing. Docker mounts this file into MySQL's initialization directory,
so it runs automatically when the MySQL volume is created for the first time.

#### Frontend and Database Connection

The Next.js route in `frontend/app/mysql/users/route.ts` uses `mysql2` and the
database values from `frontend/.env.local`. The connection flow is:

```text
Browser -> Next.js page -> /mysql/users -> mysql2 -> MySQL container
```

The browser does not connect directly to MySQL. The server-side route queries
the database and returns user records as JSON.

#### Run the Updated Frontend

From the repository root, run:

```bash
docker compose up
```

Open the frontend at [http://localhost:3000](http://localhost:3000).

Stop the services with:

```bash
docker compose down
```

To recreate the development database and rerun the SQL initialization script:

```bash
docker compose down -v
docker compose up
```

The `-v` option deletes the existing MySQL data volume.

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
- Structure: `frontend/app/` contains the root layout, page, global styles, and the MySQL users route.
- How it functions: Next.js serves the page and handles the server-side database request through the `/mysql/users` route.

### Database Backend

The database backend stores the files required to initialize MySQL.
- `frontend/.env.example`: An environment template with placeholder database values.
- `Database Backend/test_SQL_Database.sql`: A MySQL script that creates the initial database, table, and sample users.

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

