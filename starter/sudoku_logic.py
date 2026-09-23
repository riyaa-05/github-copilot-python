import copy
import random

# Copilot-assisted review: the single-solution validation logic and puzzle-removal
# strategy were reviewed to ensure the generator still satisfies the uniqueness requirement.

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def _find_empty_cell_with_fewest_candidates(board):
    best_cell = None
    best_candidates = None

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != EMPTY:
                continue

            candidates = [
                candidate
                for candidate in range(1, SIZE + 1)
                if is_safe(board, row, col, candidate)
            ]
            if not candidates:
                return (row, col), []
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_cell = (row, col)
                best_candidates = candidates
                if len(best_candidates) == 1:
                    return best_cell, best_candidates

    return best_cell, best_candidates or []


def _is_valid_completed_board(board):
    expected = set(range(1, SIZE + 1))
    return (
        all(set(row) == expected for row in board)
        and all(
            {board[row][column] for row in range(SIZE)} == expected
            for column in range(SIZE)
        )
        and all(
            {
                board[row][column]
                for row in range(box_row, box_row + 3)
                for column in range(box_column, box_column + 3)
            }
            == expected
            for box_row in range(0, SIZE, 3)
            for box_column in range(0, SIZE, 3)
        )
    )


def count_solutions(board, limit=2):
    """Count board solutions, stopping when ``limit`` solutions are found."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    cell, candidates = _find_empty_cell_with_fewest_candidates(board)
    if cell is None:
        return int(_is_valid_completed_board(board))
    if not candidates:
        return 0

    row, col = cell
    solutions = 0
    for candidate in candidates:
        board[row][col] = candidate
        solutions += count_solutions(board, limit)
        board[row][col] = EMPTY
        if solutions >= limit:
            return solutions
    return solutions


def remove_cells(board, clues):
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    target_removals = SIZE * SIZE - clues
    removed = 0

    for row, col in cells:
        if removed >= target_removals:
            break

        value = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(board) == 1:
            removed += 1
        else:
            board[row][col] = value

    return removed

def generate_puzzle(clues=35):
    if not 0 <= clues <= SIZE * SIZE:
        raise ValueError(f"clues must be between 0 and {SIZE * SIZE}")

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
