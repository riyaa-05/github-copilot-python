import app as app_module


def test_index_returns_the_game_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sudoku" in response.data


def test_new_game_returns_a_puzzle_with_default_clue_count(client):
    response = client.get("/new")

    assert response.status_code == 200
    payload = response.get_json()
    assert "puzzle" in payload
    assert sum(
        cell != 0
        for row in payload["puzzle"]
        for cell in row
    ) == 35


def test_new_game_rejects_invalid_clue_count(client):
    response = client.get("/new?clues=not-a-number")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Clues must be a number"}


def test_check_returns_an_error_before_a_game_starts(client):
    app_module.CURRENT.update(puzzle=None, solution=None)

    response = client.post("/check", json={"board": []})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No game in progress"}


def test_check_rejects_a_malformed_board(client):
    app_module.CURRENT.update(
        puzzle=None,
        solution=[[1] * 9 for _ in range(9)],
    )

    response = client.post("/check", json={"board": []})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Board must be a 9x9 grid of numbers"}


def test_check_returns_empty_incorrect_cells_for_the_current_solution(client):
    app_module.CURRENT.update(
        puzzle=None,
        solution=[
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
        ],
    )

    response = client.post("/check", json={"board": app_module.CURRENT["solution"]})

    assert response.status_code == 200
    assert response.get_json() == {"incorrect": []}


def test_check_reports_incorrect_cells(client):
    app_module.CURRENT.update(
        puzzle=None,
        solution=[[1] * 9 for _ in range(9)],
    )
    board = [[1] * 9 for _ in range(9)]
    board[2][4] = 9

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.get_json() == {"incorrect": [[2, 4]]}


def test_check_ignores_empty_cells(client):
    app_module.CURRENT.update(
        puzzle=[[0] * 9 for _ in range(9)],
        solution=[[1] * 9 for _ in range(9)],
    )

    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_hint_returns_one_empty_non_prefilled_cell(client):
    puzzle = [[0] * 9 for _ in range(9)]
    puzzle[0][0] = 9
    solution = [[1] * 9 for _ in range(9)]
    app_module.CURRENT.update(puzzle=puzzle, solution=solution)

    response = client.post('/hint', json={'board': puzzle})

    assert response.status_code == 200
    assert response.get_json() == {'row': 0, 'col': 1, 'value': 1}


def test_hint_does_not_overwrite_filled_cells(client):
    puzzle = [[0] * 9 for _ in range(9)]
    solution = [[1] * 9 for _ in range(9)]
    app_module.CURRENT.update(puzzle=puzzle, solution=solution)
    board = [[2] + [0] * 8] + [[0] * 9 for _ in range(8)]

    response = client.post('/hint', json={'board': board})

    assert response.status_code == 200
    assert response.get_json()['row'] == 0
    assert response.get_json()['col'] == 1
