#!/usr/bin/env python3
"""Define Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialization Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user with email and password
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """valid user email and password
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        # if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
        #     return True
        return False

    def create_session(self, email: str) -> str:
        """create session for user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = str(_generate_uuid())
        user.session_id = session_id
        self._db._session.commit()
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """returns the corresponding User or None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroy a session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """get reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update password
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        hash_pass = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hash_pass,
                             reset_token=None)
