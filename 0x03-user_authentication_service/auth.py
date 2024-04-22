#!/usr/bin/env python3
"""Define Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound, InvalidRequestError


def _hash_password(password: str) -> bytes:
    """hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pass = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pass)
            return new_user
        raise ValueError(f'User {email} already exists')
