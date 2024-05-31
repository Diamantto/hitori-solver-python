"""This module contains the utility functions for the authentication process."""
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated, Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from auth.models import TokenData, UserLogin
from database import DB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def verify_password(plain_password, hashed_password):
    """Verify the password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash the password"""
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    """Authenticate the user"""
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user


async def get_user(username: str):
    """Get the user"""

    # Query the collection to find the user by username
    user = await DB['users'].find_one({'username': username})

    if user:
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "hashed_password": user["hashed_password"]
        }


async def create_user(user_data: UserLogin):
    """User create function."""
    # Access the 'users' collection
    collection = DB['users']

    # Check if the username already exists
    existing_user = await collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this username already exists.")

    # Insert the new user into the collection
    user_doc = await collection.insert_one({
        "username": user_data.username,
        "hashed_password": get_password_hash(user_data.password)
    })

    return str(user_doc.inserted_id)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get the current user by validating the token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create the access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
