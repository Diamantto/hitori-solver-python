"""Test endpoints"""
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app
from test.consts_input import input_puzzle_5x5
from test.test_solver import puzzle_5x5_solution

# Create a test client using the TestClient class provided by FastAPI
test_client = TestClient(app=app)


# def test_solve_matrix_valid_input(user_token):
#     """Test for solving a matrix."""
#     # Define valid input data
#     valid_data = {"puzzle": input_puzzle_5x5}
#
#     # Send POST request to /solve endpoint with valid data
#     headers = {"Authorization": f"Bearer {user_token}"}
#     response = test_client.post("/api/solve", json=valid_data, headers=headers)
#
#     # Assert that the response status code is 200
#     assert response.status_code == 200
#
#     # Assert that the response contains the expected data (e.g., result of solving the matrix)
#     data = response.json()
#     solution = data['solution']
#     assert puzzle_5x5_solution == solution
#
#
# def test_solve_matrix_invalid_input(user_token):
#     """Test for solving a matrix."""
#     # Define invalid input data
#     invalid_data = {"puzzle": [[1, 2, 3], [4, 5, 6]]}
#
#     # Send POST request to /solve endpoint with invalid data
#     headers = {"Authorization": f"Bearer {user_token}"}
#     response = test_client.post("/api/solve", json=invalid_data, headers=headers)
#
#     # Assert that the response status code is 400 (Bad Request)
#     assert response.status_code == 400
#     print("response.text", response.text)
#     # Assert that the response contains the expected error message
#     assert "Usage: Puzzle should be size N x M" in response.text


@pytest.mark.asyncio
async def test_generate_rooms_valid_input(user_token):
    """Test for generating rooms with valid input."""
    # Define valid input data (e.g., number of rooms)
    valid_num = 5
    # Send GET request to /generate endpoint with valid input
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/api/generate", headers={"Authorization": f"Bearer {user_token}"},
            params={"size": valid_num},
        )

    # Assert that the response status code is 200
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generate_rooms_invalid_input(user_token):
    """Test for generating rooms with invalid input."""
    # Define invalid input data (e.g., negative number of rooms)
    invalid_num = -1
    # Send GET request to /generate endpoint with invalid input

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/api/generate", headers={"Authorization": f"Bearer {user_token}"},
            params={"size": invalid_num},
        )

    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
    # Assert that the response contains the expected error message
    assert "Size should be greater than 1" in response.text
