"""Models for auth process."""
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """User model"""
    id: str
    username: Optional[str] = None
    hashed_password: str


class Token(BaseModel):
    """Token model"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model"""
    username: str


class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str
