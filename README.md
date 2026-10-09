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
- Python packages from `machine_learning/python_requirements.txt`:
  - numpy
  - torch
  - pytest
  - pylint
  - matplotlib

#### Gilded_Guild_Alpha Requirements
- Unity Hub
- Unity 6000.1.12f1

#### Additional Frontend Dependencies
The frontend now also includes support for password hashing, secure session handling, database access, and Unity WebGL embedding:
- `bcryptjs` for password hashing and verification
- `iron-session` for authenticated session management
- `mysql2` for MySQL connectivity from Next.js server routes
- `react-unity-webgl` for embedding and controlling the Unity game client

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
SESSION_SECRET=your_example_secret
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

### Run Timmy Model
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest
python -m machine_learning.agents.agent_timmy

## Architecture Overview

The repository is organized into four areas: the frontend, backend, Unity code, and machine learning training environment.

### Frontend

The frontend is an App Router Next.js application built with TypeScript and React.

- Framework: Next.js 16 with React 19 and React DOM.
- Styling and tooling: Tailwind CSS 4, PostCSS, ESLint 9, and TypeScript 5.
- Structure: `frontend/app/` contains the application shell, route handlers, and server-side database access.
- Session and auth: `bcryptjs` and `iron-session` support password hashing and authenticated user sessions.
- Database access: `mysql2` is used from server-side route handlers to read data from the MySQL container.
- Unity integration: `react-unity-webgl` allows the frontend to embed and control the Unity WebGL game experience.
- public/WebGL Build contains a version of the Gilded Guild game, which can be run via the application

### Database Backend

The project includes a MySQL initialization workflow so the app can start with a ready-to-use schema.

- `frontend/.env.example` provides the expected environment variables.
- `Database Backend/test_SQL_Database.sql` creates the database, users table, and sample records used during local development.
- Docker Compose brings up both the database container and the frontend so the app can connect through the app route layer.

### Gilded_Guild_Alpha

The Unity project remains the game client and gameplay foundation for the system.

- The project under `Gilded_Guild_Alpha` contains the Unity scenes, scripts, and assets used for the game itself.
- The current structure supports lobby and gameplay screens, with networking and game logic organized under the Unity `Assets` folder.
- The game is designed to be embedded into the web frontend for a browser-based experience, while still being developed as a full Unity project.

### Machine Learning

The machine learning portion is organized as a Python training and simulation space.

- `machine_learning/game_files` contains the Gymnasium-style environment used for training and testing game logic.
- `machine_learning/tests` includes the testing utilities and unit tests that validate basic game actions.
- `machine_learning/agents` is the intended home for different bot strategies and model variants.
- `machine_learning/models` will hold trained models produced by the agents.
- Python dependencies include `numpy`, `torch`, `pytest`, `pylint`, and `matplotlib` to support training, testing, and analysis work.


