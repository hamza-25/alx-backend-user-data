#!/usr/bin/env python3
"""Define Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid(self) -> str:
    """return a string representation of a new UUID
    """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """valid user email and password
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """create session for user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
