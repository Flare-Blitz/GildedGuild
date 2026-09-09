- Date:
    Prompter:
    Model Used:
    Prompt:
    AI Output:
    My Modifications:

- Date: 2026-05-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: I want to create an application where I can play the board game Splendor in Python. The game should be a text game, and it should also be formatted so that I can use it for training neural networks, or where a human can play against it. How should I format the game file to accommodate this?
    AI Output: Recommended organizing Splendor as its own game module and class rather than mixing it with the existing Connect4 files. The game class should contain the board state and rules, while separate methods handle resetting, stepping through structured actions, returning fixed-size training states, listing legal actions, and rendering text for human play. Human input and neural-network actions should both be converted into the same stable action format.
    My Modifications: I sorted the project so the existing Connect4 files remain under `TestProjects/Connect4/`, while the new general machine-learning game work belongs under `MachineLearning/`. The empty `MachineLearning/game.py` can serve as the starting point for the Splendor game module.

- Date: 2026-09-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: How is a json file formatted?
    AI Output: Explained JSON objects, arrays, strings, numbers, booleans, null values, nesting, and syntax rules such as double-quoted keys and no trailing commas.
    My Modifications: I created `MachineLearning/GameFiles/cards.json` as a JSON array of card objects, using fields for level, color, points, and gem costs.

- Date: 2026-09-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Use my existing formatting and your research into what the standard Splendor deck looks like to fill out my cards.json file. There should be a total of 90 cards, 18 cards of each color and 40 level 1 cards, 30 level 2 cards, and 20 level 3 cards.
    AI Output: Explained that the exact copyrighted deck list could not be reproduced, and suggested manually transcribing it from an authorized source or creating a custom balanced deck.
    My Modifications: I populated `MachineLearning/GameFiles/cards.json` with 90 card records in the project's implementation format. The dataset contains 40 level 1 cards, 30 level 2 cards, 20 level 3 cards, and 18 cards for each of the five colors. I also used uppercase field names and single-letter color codes, which `GameFiles/game.py` normalizes when loading cards into `Card` objects. I based it off of existing JSON Lists

- Date: 2026-07-16
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Write a function to display the cards in the current turn player's hand, and add the function to the board Display function. Modify the display functions of the other players to show the level of each card in their hand.
    AI Output: Suggested adding a `Player.render_hand` function, rendering the current player's cards with `Card.render`, and showing compact level labels for the other players in `Board.display`.
    My Modifications: The actual version includes `Player.render_hand` and calls it from `Board.display`. The current player's hand is rendered as cards, while other players' hands are shown as level labels such as `L1` and `L2`.

- Date: 2026-07-16
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Make the hand of the turn player look like the card displays, with the card outline, and colors indicating the cost of each color, the color of the card, and the point total.
    AI Output: Suggested extending the card renderer and combining rendered card lines horizontally for the current player's hand.
    My Modifications: The actual version uses the existing `Card.render` output for hand cards, including the box outline, colored cost values, the colored card symbol, point total, and level label. The hand renderer pads cards before joining them so multiple cards align horizontally.

- Date: 2026-07-16
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Don't display the turn player's hand next in the player info section, create a separate section for displaying the current turn's hand, so that you can make it take up the multiple lines it uses without looking inconsistent with the other players.
    AI Output: Suggested removing the active player's multi-line hand from the player summary loop and adding a separate current-turn hand section below the player information.
    My Modifications: The actual version has a `CURRENT TURN HAND` section after `PLAYERS`. Other players retain one-line hand level summaries, and the current player's multi-line card display is printed only in the dedicated section.

- Date: 2026-07-16
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Now, want to add the ability for a player to purchase a reserved card in their hand. The input should be P H [Card Spot]. it should then run a function to purchase the card, taking the money if they can afford it and returning to the gem pile, exactly the same as the existing function to purchase a card.
    AI Output: Suggested extracting shared affordability and gem-transfer logic into `_purchaseCard`, adding `buyHandCard`, removing the purchased card from the hand, and routing `P H [Card Spot]` through `processHumanAction`.
    My Modifications: The actual version contains `_purchaseCard` and `buyHandCard`, so reserved-card purchases can use the same payment logic and return gems to the pile. The current checked-in parser still uses the older fixed-position command parsing and does not yet accept the spaced `P H [Card Spot]` command, so that portion of the suggestion remains unfinished.

- Date: 2026-08-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: How can I fix render_hand to have consistent spacing between the cards across individual lines for the turn player
    AI Output: Explained that ANSI color escape sequences were being counted by `len()` even though they have no visible terminal width. Suggested measuring visible text width by stripping ANSI sequences and padding each card line based on that visible width before joining the cards horizontally.
    My Modifications: I changed `render_hand` to use a fixed card width of 12 characters and pad each rendered line to that width before joining the cards with two spaces.

- Date: 2026-08-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: I have developed a program that lets a player play Splendor, but I want to determine a function that makes the bot take a random action. Give me some ideas for how I can implement this, and if I would need to update my functions to better process random actions.
    AI Output: Recommended generating legal random actions from the current board state and routing them through the existing action-processing logic. Identified the need to account for available gems, occupied board cards, reserved cards, hand capacity, and valid deck reservations. Also identified several unrelated blockers that should be fixed before testing random actions.
    My Modifications: I have not started implementing the random move feature. Instead, I began refactoring and designing how moves should be processed through a shared action system for both human and bot players.

- Date: 2026-08-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Elaborate on point 5, what issues do I have?
    AI Output: Explained the execution blockers affecting the game, including the empty `takeRandomAction` function, conflicting quotation marks in `GemPile.__str__`, the incorrect top-deck reservation call, the victory-check condition and player-name mismatch, and crashes caused by empty input.
    My Modifications: I have not started implementing the random move feature. Instead, I continued reviewing the existing move-processing flow and identifying changes needed to support a shared action system.

- Date: 2026-08-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: What would structured actions look like? How would I take the existing process human action function and convert it into one that runs a universal ExecuteAction?
    AI Output: Recommended separating human-input parsing from game-state mutation. Human commands should be converted into a structured `Action` object, and both human and bot actions should then be passed to a universal `executeAction` function that dispatches to the appropriate board method.
    My Modifications: I have not started implementing the random move feature. I refactored the design of move processing so human input and future bot actions can use the same execution path.

- Date: 2026-08-06
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Should the action be unstructured, or should I create a new class for it?
    AI Output: Recommended creating a structured immutable `Action` dataclass with an action type and optional fields for colors, level, and row. This provides a consistent interface for human parsing, random bots, and future machine-learning agents.
    My Modifications: I have not started implementing the random move feature. I focused on refactoring the move-processing design around a structured action class and a universal action executor.

- Date: 2026-09-07
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: I'm learning how to use PyLint, can you show me how I can view the Pylint github action workflow errors in VsCode?
    AI Output: Explained how to use the GitHub Actions extension and the Problems panel in VS Code to view workflow logs and local Pylint diagnostics. Clarified that the current workflow reports errors in the GitHub Actions log rather than directly in the Problems panel.
    My Modifications: I reviewed the workflow and learned how to inspect Pylint results locally and through GitHub Actions.

- Date: 2026-09-07
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: How can I configure pylint to change numbers, such as the number of attributes alloted for a class?
    AI Output: Explained that Pylint design limits such as `max-attributes` can be configured in `.pylintrc` under `[DESIGN]` or in `pyproject.toml` under `[tool.pylint.design]`. Also explained how to override a setting temporarily from the command line.
    My Modifications: I learned how to configure Pylint design thresholds for the project.

- Date: 2026-09-07
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: What is the best practice location to place the file in my current directory, it seems weird to me for it to be its own dedicated file in the root folder
    AI Output: Recommended keeping a root-level `.pylintrc` because it applies consistently to the repository and GitHub Actions. Also described using a root-level `pyproject.toml` as a modern alternative.
    My Modifications: I considered where shared Pylint configuration should live in the repository.

- Date: 2026-09-07
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Is it good practice to have three different pylints running, on three different versions?
    AI Output: Explained that running the same lint command across multiple Python versions is usually unnecessary because linting and runtime compatibility testing serve different purposes. Recommended running Pylint once with a pinned version and using a matrix for tests.
    My Modifications: Removed version 3.8, as some of the code I used was depreciated, and it was no longer supported.

- Date: 2026-09-07
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Python 3.9 doesn't support the level and row declaration of the Action object, should I refactor my code to work with 3.9, and how difficult of a fix would it be? I currently check version 3.9 for pylint.
    AI Output: Explained that `int | None` requires Python 3.10, while `tuple[str, ...]` is supported in Python 3.9. Recommended using `Optional[int]` and keeping Python 3.9 support because the GitHub Actions workflow tests Python 3.9.
    My Modifications: Updated the Action annotations to use `Optional[int]`.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Should my ESLint configuration be in a different workflow file from Pylint? Insert this prompt into my AI_Usage_Log.md file, outline how I modified the Pylint linter to be a more generic ci.yml, and added ESLint to the flow.
    AI Output: Recommended keeping ESLint and Pylint in the same CI workflow when they are both used for pull-request validation. Suggested organizing them as separate jobs in a shared `ci.yml`, while reserving separate workflow files for tasks with different triggers, permissions, or lifecycles.
    My Modifications: I updated the Pylint workflow into a more generic `ci.yml` workflow and added ESLint as a separate linting job within the same CI pipeline.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: I'm setting up a linter for github: eslint $(git ls-files '*.js'), what is my solution to get around this issue, do I need to update my linter?
    AI Output: Explained that the workflow was installing the latest global ESLint, which could be ESLint 10, while the project dependencies use ESLint 9 and `eslint-plugin-react@7.37.5`. Recommended changing to the `frontend` working directory, running `npm ci` to install the lockfile-pinned dependencies, and running `npm run lint` so the local ESLint executable is used.
    My Modifications: I followed the commands by navigating to `frontend` and running `npm ci`, installing the proper project dependencies. I updated the GitHub Actions ESLint job to use `npm ci` and `npm run lint` instead of installing ESLint globally and calling `eslint $(git ls-files '*.js')`.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: How can I verify that the linter is working?
    AI Output: Recommended running `npm run lint` from the `frontend` directory, checking the installed versions with `npx --no-install eslint --version` and `npm ls eslint eslint-plugin-react`, and verifying that an intentionally invalid stdin example produces a nonzero exit code.
    My Modifications: I ran `npm ci` from the `frontend` directory to install the correct dependencies. I can verify the linter with `npm run lint` and confirm that the local ESLint version is being used with `npx --no-install eslint --version`.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: I want to create unit tests for the game.py file, using pytest
    AI Output: Recommended building focused pytest coverage for value objects, decks, board state transitions, and action processing. Identified that `Game()` originally entered an interactive loop and that deck loaders depended on the repository root as the working directory.
    My Modifications: I started setting up pytest for `MachineLearning/GameFiles/game.py` and created an initial test fixture file.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: how would I organize the tests, within the game_test file?
    AI Output: Suggested organizing tests by implementation layer: value objects, rendering, resources and decks, board setup, board actions, game rules, and action processing.
    My Modifications: I planned the test file around the classes and methods in `game.py`, using descriptive test names and section comments.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Why does import pytest not work?
    AI Output: Explained that Pylance could not resolve `pytest` because it was not installed in the workspace's `.venv`, and recommended selecting the virtual environment in VS Code and installing pytest there.
    My Modifications: I installed pytest with `./.venv/bin/python -m pip install pytest` and selected the local virtual environment for the project.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Do I need docstrings for test functions, if so, how would I write a good docstring?
    AI Output: Explained that pytest does not require test docstrings, but concise docstrings are useful for tests involving non-obvious rules or setup. Recommended prioritizing descriptive test names.
    My Modifications: I kept docstrings for fixtures and planned to use them selectively for tests with complex behavior.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: What about pylint, it is creating warnings due to no docstrings
    AI Output: Explained the `missing-function-docstring` warning and recommended either adding concise docstrings or disabling that warning for the test module.
    My Modifications: I added a module docstring and disabled `missing-function-docstring` in the test file.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: What would a helper to create a non-interactive game instance look like. elaborate what that would do.
    AI Output: Recommended temporarily replacing `Game.play()` with a no-op using pytest's `monkeypatch` fixture while constructing `Game`, so the constructor would not start the interactive loop.
    My Modifications: I changed `Game.__init__()` in `game.py` so it creates the board without automatically calling `play()`, making normal test construction non-interactive.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Create all necessary fixtures for the classes. Dont create any tests yet, just design the fixtures and elaborate on any complexity the fixtures hold.
    AI Output: Designed reusable fixtures for costs, cards, tiles, players, resources, gem piles, decks, boards, games, and structured actions. Recommended controlling randomness and the working directory for JSON fixture loading.
    My Modifications: I added reusable fixtures to `game_test.py`, including `repository_root`, `deterministic_random`, `game_files_cwd`, model objects, resource variants, deterministic decks and boards, a non-interactive game, and action objects.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Why are you formatting it like it is just fixtures, when I plan on adding tests to the file
    AI Output: Clarified that the fixture-only wording reflected the immediate request, and recommended the future-oriented module docstring `Unit tests and shared fixtures for the game module`.
    My Modifications: I changed the module docstring to `Unit tests for the game module` to reflect the file's eventual purpose.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: explain to me what mokeypatch is
    AI Output: Explained that pytest's `monkeypatch` fixture temporarily changes attributes, functions, or the working directory and automatically restores them after the test.
    My Modifications: I used `monkeypatch` to make random deck setup deterministic and to change to the repository root while loading JSON data.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Since I modified Game to not run play, would that fixture be unnecesary?
    AI Output: Confirmed that the `monkeypatch` dependency in the `game` fixture was no longer necessary once `Game.__init__()` stopped calling `play()`.
    My Modifications: I removed `monkeypatch` from the `game` fixture while retaining `game_files_cwd` and `deterministic_random`.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: why is monkeypatch being declared in function declarations
    AI Output: Explained pytest fixture dependency injection: declaring `monkeypatch` as a parameter asks pytest to provide its temporary patching tools. Also clarified that unused fixture parameters can still be intentional dependencies when they provide setup side effects.
    My Modifications: I retained `monkeypatch` only in fixtures that directly use it and removed it from the `game` fixture after the constructor change.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: what about some of these fixtures that are being declared in functions but never used? I'm getting pylance warnings, are these function parameters like game_files_cwd actually doing something?
    AI Output: Explained that pytest fixture parameters such as `game_files_cwd` and `deterministic_random` are dependencies used for their setup side effects, even when their names do not appear in the function body. Pylance does not fully understand this pytest pattern.
    My Modifications: I kept those fixture parameters because they configure the working directory and randomness required by the game loaders.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: how can I remove the warnings then?
    AI Output: Recommended suppressing `reportUnusedParameter` for the test module with a Pyright directive and disabling Pylint's unused-argument warning only where needed, while keeping meaningful pytest fixture dependencies.
    My Modifications: I added `# pylance: reportUnusedParameter=false` and retained the fixture dependency names so pytest can inject them.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Why redefining name 'repository_root' from outer scope (line 26)\n\nWhy is this happening, and should I be concerned
    AI Output: Explained Pylint warning `redefined-outer-name` as a false positive caused by pytest injecting a fixture named `repository_root` into another fixture with the same name.
    My Modifications: I added `# pylint: disable=redefined-outer-name` to the test module because the repeated name is intentional pytest fixture injection.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: These fixtures are taking up a lot of space, should I have a separate file for the actual tests?
    AI Output: Recommended moving shared fixtures to pytest's `conftest.py` and keeping behavior-focused tests in `game_test.py`, with the option to split models, board, and action tests into separate files as the suite grows.
    My Modifications: I creates a conftest.py file, and moved all the fixtures there