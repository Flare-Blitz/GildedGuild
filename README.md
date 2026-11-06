# GildedGuild
This is a repository housing the code for the GildedGuild Senior Design Project. When completed, it will allow users to run a react application that allows them to play a game programmed in unity against machine learning bots trained in a python gymnasium.

## Getting Started:

### Requirements
- Git
- Docker
- Docker Compose

#### Frontend Requirements
- Node.js 20.9 or later and npm (CI uses Node.js 20; Docker Compose uses Node.js 24)
- npm

#### Machine Learning Python File Requirements
- Python 3.10 (the version used by CI)
- pip and the packages listed in `machine_learning/python_requirements.txt`:
  - `numpy`
  - `torch`
  - `pytest`
  - `pylint`
  - `matplotlib`

#### Gilded_Guild_Alpha Requirements
- Unity Hub
- Unity 6000.1.12f1

#### Additional Frontend Dependencies
The frontend's direct runtime dependencies include UI components and styling, theme support, icons, and integration with authentication, MySQL, and the Unity WebGL client:
- `@chakra-ui/react`, `@emotion/cache`, and `@emotion/react` for UI components and styling
- `bcryptjs` for password hashing and verification
- `iron-session` for authenticated session management
- `mysql2` for MySQL connectivity from Next.js server routes
- `next-themes` for theme support
- `react-icons` for icons
- `react-unity-webgl` for embedding and controlling the Unity game client

The frontend uses Next.js, React, and React DOM. Its development tools include TypeScript, ESLint, Tailwind CSS, and PostCSS; npm installs these from `frontend/package-lock.json`.

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
DB_NAME=GildedGuildDatabase
DB_PORT=3306
SESSION_SECRET=your_example_secret
```

The two password values must match. Do not commit either `.env` or
`frontend/.env.local`.

#### SQL Database Initialization

The file `Database Backend/GildedGuildDatabase.sql` creates the `GildedGuildDatabase` database,
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

### Machine Learning Gymnasium

The machine_learning folder features all of the code used to train bots to play
the GildedGuild game

#### Install dependencies:
- python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest

#### Play a preset game against Timmy, Spike, and Johnny
from root directory
- python -m machine_learning.main

### Train an agent
- Agent files: agent_timmy, agent_steve, agent_johnny, agent_spike, agent_quentin
python -m machine_learning.agents."REPLACE_WITH_AGENT_FILE"

## Architecture Overview

The repository is organized into four areas: the frontend, backend, Unity code, and machine learning training environment.

### Frontend

The frontend is an App Router Next.js application built with TypeScript and React.

- `frontend/app/` contains the home, login, registration, and game pages, as well as server actions, session utilities, and data-access helpers.
- Login, registration, guest access, and logout are handled by server actions. `iron-session` manages sessions, and `bcryptjs` hashes and verifies passwords.
- `frontend/app/mysql/users/route.ts` provides a server-side MySQL route using `mysql2`; database credentials are read from the frontend environment.
- The game page embeds the WebGL build in `frontend/public/WebGL Build/` and uses `react-unity-webgl` to pass player information to Unity.
- The UI uses Chakra UI and Emotion, with theme and icon support from `next-themes` and `react-icons`.
- Docker Compose runs the frontend in the Node.js 24 container. The frontend package manifest and lockfile define its runtime and development dependencies.

### Database Backend

`Database Backend/GildedGuildDatabase.sql` creates the `GildedGuildDatabase` schema and its `parents`, `users`, `bot`, `gamestats`, and `participants` tables, including their keys and relationships. It also inserts sample development records.

Docker Compose starts MySQL 8.4 and mounts this SQL file into MySQL's initialization directory. MySQL runs it when initializing a new data volume; the named `mysql_data` volume preserves database contents between container runs. The frontend connects to the database through server-side Next.js code using the values in `frontend/.env.local`, based on `frontend/.env.example`.

You can view the database schema at Documentaion -> ERD Diagram.png

### Gilded_Guild_Alpha

The Unity project remains the game client and gameplay foundation for the system.

- The project under `Gilded_Guild_Alpha` contains the Unity scenes, scripts, and assets used for the game itself.
- The current structure supports lobby and gameplay screens, with networking and game logic organized under the Unity `Assets` folder.
- The game is designed to be embedded into the web frontend for a browser-based experience, while still being developed as a full Unity project.

### Machine Learning

The `machine_learning` package contains the Python game simulation, agent implementations, saved model files, evaluation outputs, and tests.

- `machine_learning/main.py` runs a preset game with the Timmy, Spike, and Johnny policies.
- `machine_learning/game_files/` contains the internal logic for running the gymnasium to train the agents, including all object definitions required to play GildedGuild
- `machine_learning/agents/` contains the individual agent entry points and shared policy, model, and state-encoding code.
- `machine_learning/agents/model/` stores the PyTorch `.pth` weights loaded by the policies; `machine_learning/agents/onnx_model/` contains ONNX model files, which are used for getting the model data in the Unity application.
- `machine_learning/agents/model_evaluation/` contains the code used to evaluate the models, and the resulting graphs generated.
- `machine_learning/tests/` contains the Python test suite for game and agent behavior. Dependencies are listed in `machine_learning/python_requirements.txt`.

### Documentation
- `AI_USAGE_LOG.md` contains all prompts to generative AI that were directly used to help create this project
- `DeveloperGuide.md` provides additional notes for how to utilize the codeabase
- `ERD Diagram` contains the original database concept
- `UPDATED ERD Diagram` contains the current Entity Relationship Diagram
- `ML_STATE_ENCODING` outlines what the output of the encode_board function in the machine_learning gymnasium represents. It outlines what each value of the tensor corresponds to in the current board state.

## .github
Contains github actions to be performed for every pull request, currently it contains:
- ESLint check (including light Cypress E2E testing)
- Pylint python syntax
- Pytest python test cases
- TruffleHog security scanning
