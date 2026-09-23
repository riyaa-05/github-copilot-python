import sudoku_logic


def test_create_empty_board_has_nine_empty_rows():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_generate_puzzle_returns_valid_solution_and_requested_clues():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert all(
        1 <= cell <= sudoku_logic.SIZE
        for row in solution
        for cell in row
    )
    assert sum(
        cell != sudoku_logic.EMPTY
        for row in puzzle
        for cell in row
    ) == 35


def test_generated_solution_has_valid_rows_columns_and_boxes():
    _, solution = sudoku_logic.generate_puzzle()
    expected = set(range(1, sudoku_logic.SIZE + 1))

    assert all(set(row) == expected for row in solution)
    assert all(
        {solution[row][column] for row in range(sudoku_logic.SIZE)} == expected
        for column in range(sudoku_logic.SIZE)
    )
    assert all(
        {
            solution[row][column]
            for row in range(box_row, box_row + 3)
            for column in range(box_column, box_column + 3)
        } == expected
        for box_row in range(0, sudoku_logic.SIZE, 3)
        for box_column in range(0, sudoku_logic.SIZE, 3)
    )


def test_generated_puzzle_has_exactly_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=35)

    assert sudoku_logic.count_solutions(puzzle) == 1


def test_puzzle_prefilled_values_match_completed_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert all(
        puzzle[row][column] in (sudoku_logic.EMPTY, solution[row][column])
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )
