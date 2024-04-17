#!/usr/bin/env python3
"""Define SessionAuth  Module
"""
from .auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Define SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session for users by id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
