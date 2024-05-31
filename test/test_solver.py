import pytest

from solver.hitori_utils import InvalidInputError
from solver.solver import HitoriSolver

puzzle_5x5_solution = [
    ['B', 2, 5, 1, 'B'],
    [2, 'B', 3, 'B', 4],
    [4, 1, 2, 5, 3],
    [3, 5, 4, 'B', 2],
    ['B', 3, 'B', 4, 5],
]

puzzle_7x7_solution = [
    ['B', 1, 2, 3, 5, 4, 7],
    [1, 8, 3, 9, 7, 2, 4],
    [2, 4, 7, 1, 3, 9, 5],
    [3, 'B', 4, 'B', 6, 1, 2],
    [4, 5, 8, 2, 'B', 7, 1],
    [7, 6, 5, 4, 2, 'B', 3],
    [6, 2, 9, 5, 1, 3, 'B']
]


def test_solution_matrix_5x5(solution_5x5):
    """
    Validate the solution for 5x5 matrix
    """
    result_data = solution_5x5.solve_hitori()
    assert 'counter' in result_data
    assert 'solution' in result_data
    solved_puzzle = result_data['solution']
    assert puzzle_5x5_solution == solved_puzzle


def test_solution_matrix_7x7(solution_7x7):
    """
    Validate the solution for 7x7 matrix
    """
    result_data = solution_7x7.solve_hitori()
    assert 'counter' in result_data
    assert 'solution' in result_data
    solved_puzzle = result_data['solution']
    assert puzzle_7x7_solution == solved_puzzle


different_rows_and_cols = [
    [1, 2, 5, 1, 4],
    [2, 4, 3, 2, 4],
    [4, 1, 2, 5, 3],
    [3, 5, 4, 1, 2],
    [2, 3, 2, 4, 5, 7]  # Unsolved puzzle
]


def test_solution_different_amount_of_rows_and_columns():
    """Test that raises InvalidInputError if
        the amount of rows and columns of the matrix are not equal"""
    with pytest.raises(InvalidInputError) as exc_info:
        HitoriSolver(different_rows_and_cols).solve_hitori()
    assert str(
        exc_info.value) == "Usage: Puzzle should be size N x M"


invalid_type = [
    [1, 2, 5, 1, 4],
    [2, 4, 3, 'b', 4],
    [4, 1, 2, 5, 3],
    [3, 5, 4, 1, 2],
    [2, 3, 2, 4, 5]
]


def test_solution_invalid_type():
    """Test that raises TypeError if input values are not integers"""
    with pytest.raises(TypeError) as exc_info:
        HitoriSolver(invalid_type).solve_hitori()
    assert str(
        exc_info.value) == "Value should be an integer"


value_zero = [
    [1, 2, 5, 1, 4],
    [2, 4, 3, 0, 4],
    [4, 1, 2, 5, 3],
    [3, 5, 4, 1, 2],
    [2, 3, 2, 4, 5]
]


def test_solution_value_zero():
    """Test that raises ValueError if input values are 0"""
    with pytest.raises(ValueError) as exc_info:
        HitoriSolver(value_zero).solve_hitori()
    assert str(
        exc_info.value) == "Value should be positive"
