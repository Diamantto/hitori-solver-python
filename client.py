"""Client integration tests module."""

import asyncio

import httpx

from solver.hitori_utils import print_start_text, print_solution
from generators.hitori_puzzles import puzzles
from test.consts_input import input_puzzle_5x5, input_puzzle_7x7

HITORI_DATA = puzzles["5"][2]

# HITORI_DATA = input_puzzle_7x7

APP_PORT = "8000"
NEW_USER = {"username": "testuser3", "password": "testpassword3"}


async def register_user():
    """Register a new user."""
    user = {"username": NEW_USER["username"], "password": NEW_USER["password"]}
    async with httpx.AsyncClient() as client:
        print(f"http://localhost:{APP_PORT}/api/register-user")
        response = await client.post(
            f"http://localhost:{APP_PORT}/api/register-user", json=user
        )
        if response.status_code == 200:
            print(f"User registered with ID: {response.json()}")
            return True
        if response.status_code == 400:
            print(f"Error: ({response.status_code}): {response.text}")
            return True
        print(f"Error: ({response.status_code}): {response.text}")
        return False


async def get_auth_token():
    """Get authentication token."""
    async with httpx.AsyncClient() as client:
        print(f"http://localhost:{APP_PORT}/api/login")
        response = await client.post(
            f"http://localhost:{APP_PORT}/api/login",
            data={"username": NEW_USER["username"], "password": NEW_USER["password"]},
        )
        if response.status_code == 200:
            print(f"Token received: {response.json().get('access_token')}")
            return response.json().get("access_token")
        print(f"Error: ({response.status_code}): {response.text}")
        return None


async def send_data(token):
    """Send request to /solve route."""
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(
                f"http://localhost:{APP_PORT}/api/solve",
                json={"puzzle": HITORI_DATA},
                headers=headers,
            )
            if response.status_code == 200:
                data = response.json()
                iteration = data['counter']
                solution = data['solution']
                timeit(iteration, solution, "Smart")
            else:
                print(f"Error: ({response.status_code}): {response.text}")
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")


async def generate_test_data(token):
    """Send request to /generate route."""
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            params = {"size": 3}
            response = await client.get(
                f"http://localhost:{APP_PORT}/api/generate",
                headers=headers,
                params=params,
            )
            if response.status_code == 200:
                data = response.json()
                result = data["puzzle"]
                print("Test board received from /generate route")
                for row in result:
                    print(row)
            else:
                print(f"Error: ({response.status_code}): {response.text}")
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")


def timeit(idx, solution, mode: str, puzzle=None):
    # Print introductory text for solver
    if mode == "Random" and puzzle is not None:
        print_start_text(puzzle, mode)
    else:
        print_start_text(HITORI_DATA, mode)
    print_solution(idx, solution, len(HITORI_DATA[len(HITORI_DATA[0]) - 1]))


async def main():
    """Execute main loop."""
    registered = await register_user()
    # registered = True
    if registered:
        token = await get_auth_token()
        if token:
            await send_data(token)
            await generate_test_data(token)


if __name__ == "__main__":
    asyncio.run(main())
