from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    try:
        clues = int(request.args.get('clues', 35))
    except (TypeError, ValueError):
        return jsonify({'error': 'Clues must be a number'}), 400

    if not 0 <= clues <= sudoku_logic.SIZE * sudoku_logic.SIZE:
        return jsonify({'error': 'Clues must be between 0 and 81'}), 400

    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle, 'solution': solution})

@app.route('/check', methods=['POST'])
def check_solution():
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else None
    if (
        not isinstance(board, list)
        or len(board) != sudoku_logic.SIZE
        or any(
            not isinstance(row, list)
            or len(row) != sudoku_logic.SIZE
            or any(not isinstance(cell, int) for cell in row)
            for row in board
        )
    ):
        return jsonify({'error': 'Board must be a 9x9 grid of numbers'}), 400

    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != sudoku_logic.EMPTY and board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})


@app.route('/hint', methods=['POST'])
def get_hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else puzzle
    if (
        not isinstance(board, list)
        or len(board) != sudoku_logic.SIZE
        or any(
            not isinstance(row, list)
            or len(row) != sudoku_logic.SIZE
            or any(not isinstance(cell, int) for cell in row)
            for row in board
        )
    ):
        return jsonify({'error': 'Board must be a 9x9 grid of numbers'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == sudoku_logic.EMPTY and board[row][col] == sudoku_logic.EMPTY:
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': solution[row][col]
                })

    return jsonify({'error': 'No empty cells available for a hint'}), 400

if __name__ == '__main__':
    app.run(debug=True)