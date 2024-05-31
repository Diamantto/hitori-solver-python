"""Test cases for auth module."""

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from httpx import AsyncClient
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from auth.utils import create_access_token, get_current_user
from main import app


client = TestClient(app=app)


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/login",
            data={"username": "invaliduser", "password": "invalidpassword"},
        )
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_register_user_error():
    """Test register_user with invalid data."""
    user = {"username": "testuser", "password": "testpassword"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/api/register-user",
            json=user,
        )
        response = await ac.post(
            "/api/register-user",
            json=user,
        )
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test get_current_user with invalid token."""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalid_token")

    assert str(
        exc_info.value) == "401: Could not validate credentials"


@pytest.mark.asyncio
async def test_gcreate_access_token_invalid():
    """Test create_access_token with invalid data."""
    token = create_access_token(data={"sub": "user_not_exists"})
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token)

    assert str(
        exc_info.value) == "401: Could not validate credentials"
