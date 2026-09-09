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
    Prompt: How would I go about adding TruffleHog to my repo? I need it to be an automatic GitHub Action, as well as being able to test it locally.
    AI Output: Recommended adding a dedicated TruffleHog workflow for pull requests, pushes to the default branch, and manual runs, along with a reproducible local scanning command. Recommended pinning the GitHub Action and scanner version, scanning for verified and unknown findings, and failing CI when findings are detected.
    My Modifications: I decided to use a dedicated `.github/workflows/secrets.yml` workflow and planned to use Docker or a native CLI for local scans.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Is there anything I would need to install beforehand, such as Docker or TruffleHog?
    AI Output: Explained that GitHub Actions does not require a local Docker or TruffleHog installation. For local scanning, Docker Desktop or a native TruffleHog installation through Homebrew can be used.
    My Modifications: I chose Docker as the preferred local option while keeping native TruffleHog installation as an alternative. I plan on using Docker later, so its fine to start using it now.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: What is Docker, and why do we need it?
    AI Output: Explained that Docker runs software in standardized containers and can provide a consistent TruffleHog environment across different operating systems. Clarified that Docker is optional and that TruffleHog can also be installed directly.
    My Modifications: I learned why Docker was recommended for reproducible local secret scanning and that it is not required for GitHub Actions.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Implement TruffleHog into my created `secrets.yml`, and let me know if there is anything in addition I need to do.
    AI Output: Added a dedicated workflow that runs TruffleHog on pull requests, pushes to `main`, and manual dispatches. The workflow uses read-only repository permissions, checks out full history, pins the TruffleHog action to a commit, uses TruffleHog v3.97.4, and fails on verified or unknown findings.
    My Modifications: I created `.github/workflows/secrets.yml` and validated its YAML syntax. I still need to commit and push the workflow to GitHub, then verify its run in the Actions tab.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: What is the string of characters in the `uses` section that you are trying to add?
    AI Output: Explained that `080c22fb8ea3107163b9dbcc33396a41c518b990` is a Git commit SHA that identifies the exact TruffleHog action revision. Clarified that it is not a password, API key, or secret.
    My Modifications: I kept the commit SHA in the workflow to pin the action to a specific revision.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Is this needed?
    AI Output: Explained that the commit SHA after `trufflesecurity/trufflehog@` is not strictly required, but is recommended because it prevents the action from changing unexpectedly. Using `@main` would be simpler but less reproducible.
    My Modifications: I kept the immutable commit reference in `secrets.yml`.

- Date: 2026-09-08
    Prompter: Jackson Keeler
    Model Used: GitHub Copilot
    Prompt: Is TruffleHog all set up, and how can I verify that it works?
    AI Output: Explained how to verify the GitHub Actions workflow from the repository's Actions tab and how to run a local scan with `trufflehog git file://. --results=verified,unknown --fail`. Documented the expected exit codes for clean scans, findings, and scan errors.
    My Modifications: I ran the local TruffleHog scan from the repository root and confirmed the workflow YAML parsed successfully. I still need to push the workflow and verify its GitHub Actions run.