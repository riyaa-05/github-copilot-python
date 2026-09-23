# Sudoku Game

## Overview

This project is a browser-based Sudoku game built with Flask, HTML, CSS, and
JavaScript. It generates playable Sudoku puzzles and provides feedback and
progress tracking while the player solves them.

## Features

- Generates Sudoku puzzles with a unique solution.
- Supports Easy, Medium, and Hard difficulty levels.
- Keeps prefilled cells locked.
- Provides hints that fill a correct cell.
- Checks the current board and identifies incorrect entries.
- Detects puzzle completion.
- Tracks solving time with a timer.
- Supports dark and light modes.
- Stores and displays the top 10 scores.
- Persists scores and theme preference with `localStorage`.
- Provides a responsive, keyboard-friendly, and accessible interface.

## Technologies

- Python 3
- Flask
- JavaScript
- HTML5
- CSS3
- pytest

## Project Structure

```text
.
├── starter/
│   ├── app.py                 # Flask routes and application state
│   ├── sudoku_logic.py        # Sudoku generation and solution logic
│   ├── requirements.txt       # Python dependencies
│   ├── static/
│   │   ├── main.js             # Game interactions and browser persistence
│   │   └── styles.css          # Responsive and themed styling
│   ├── templates/
│   │   └── index.html          # Game page
│   └── tests/                  # Application and Sudoku logic tests
├── pytest.ini                  # pytest configuration
└── screenshots/                # Project screenshots
```

## Installation

1. Clone the repository and open a terminal in the repository directory.
2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   On macOS or Linux, activate it with:

   ```bash
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   pip install -r starter/requirements.txt
   ```

## Run the Application

From the repository root, run:

```bash
python starter/app.py
```

Then open <http://127.0.0.1:5000> in a web browser.

## Run the Tests

From the repository root, run the complete test suite with:

```bash
pytest
```

The test configuration in `pytest.ini` discovers tests in `starter/tests` and
adds `starter` to the Python import path.

## Testing Approach

The tests use pytest and Flask's test client. Application tests cover page
loading, puzzle creation, request validation, solution checking, and hints.
Sudoku logic tests cover board creation, valid completed solutions, requested
clue counts, matching prefilled values, and unique-solution verification.
