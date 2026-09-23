# Sudoku Project Instructions

## Project
This is a Flask-based Sudoku web application using Python, HTML, CSS, and JavaScript.

## General Guidelines
- Keep the existing project structure unless there is a clear reason to change it.
- Prefer simple, readable, maintainable code.
- Do not introduce unnecessary dependencies.
- Reuse existing functions and components where possible.
- Avoid duplicating logic.
- Keep frontend and backend responsibilities clearly separated.
- Use meaningful variable and function names.
- Add comments only where they improve understanding.

## Python Guidelines
- Use modern Python syntax and clear function definitions.
- Keep Sudoku generation and solving logic inside `sudoku_logic.py`.
- Keep Flask routes and application state inside `app.py`.
- Sudoku puzzles must have exactly one valid solution.
- Validate inputs before processing them.
- Avoid unnecessary global state.

## JavaScript Guidelines
- Keep UI interactions and browser-side game logic in `static/main.js`.
- Use localStorage for persistent leaderboard data.
- Keep timer behavior reliable when starting a new game.
- Provide immediate visual feedback for invalid entries.
- Keep DOM manipulation organized and readable.

## CSS Guidelines
- Keep styling in `static/styles.css`.
- Support both light and dark modes.
- Make the layout responsive for desktop and mobile screens.
- Use alternating visual styles for the 3x3 Sudoku boxes.
- Maintain readable contrast between text, cells, controls, and backgrounds.

## Required Features
The application must support:
- Easy, Medium, and Hard difficulty levels.
- Different numbers of prefilled cells based on difficulty.
- Sudoku puzzles with exactly one unique solution.
- Immediate feedback for invalid moves.
- A completion message when the puzzle is solved.
- A Hint button that fills and locks one correct cell.
- A Check button that highlights incorrect entries.
- A timer.
- A dark/light mode toggle.
- A Top 10 leaderboard.
- Leaderboard persistence using localStorage.
- Leaderboard entries containing name, time, and difficulty.

## Testing
- Do not remove existing tests.
- Run the test suite after significant changes.
- Fix failing tests before continuing.
- Keep test behavior predictable and deterministic where possible.

## Copilot Workflow
- Major milestones for this project were implemented with GitHub Copilot, including the puzzle generator, uniqueness validation, UI interactions, timer logic, hint/check flows, theme support, and local leaderboard storage.
- Each Copilot suggestion should be reviewed against the project requirements before being accepted.
- If a suggestion conflicts with the project requirements, prioritize the requirements over the suggestion.
- Validate the relevant tests and behavior after significant changes.
- Do not add optional features unless the required functionality is working first.
