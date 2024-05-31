"""Configuration file for pytest."""
import asyncio
import os

from test.consts_input import input_puzzle_5x5, input_puzzle_7x7

import pytest
import pytest_asyncio
from httpx import AsyncClient

from database import client
from main import app
from solver.solver import HitoriSolver


@pytest_asyncio.fixture
async def user_token():
    """Fixture to get the user token."""
    test_user = {"username": "test", "password": "123"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/api/register-user", json=test_user)
        res = await ac.post("/api/login", data=test_user, headers={
            "Content-Type": "application/x-www-form-urlencoded"})
        data = res.json()

    return data['access_token']


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    _ = client.drop_database(os.getenv('DB_NAME', 'test'))
    loop.close()


@pytest.fixture
def solution_5x5():
    """Create a Solver instance for 5x5 matrix"""
    return HitoriSolver(input_puzzle_5x5)


@pytest.fixture
def solution_7x7():
    """Create a Solver instance for 7x7 matrix"""
    return HitoriSolver(input_puzzle_7x7)
