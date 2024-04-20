#!/usr/bin/env python3
"""Define SessionAuth  Module
"""
from .auth import Auth
# from base64 import b64decode
# from typing import TypeVar
from models.user import User
from uuid import uuid4
from flask import request


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
        """return user id by session_id
        """
        # if type(session_id) is str:
        #     return self.user_id_by_session_id.get(session_id)
        #     return self.user_id_by_session_id.get(session_id)
        if session_id is None:
            return None
        if isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """returns a User instance based on a cookie value
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        # print(user_id)
        # print(self.session_cookie(request))
        # print(self.user_id_for_session_id('6810041a-1277-4258-8cb2-e7dd32df1662'))
        # print(self.user_id_by_session_id.get('a5dcf316-b73e-4758-b747-7fb18c7ca143'))
        # exit(4)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroys an auth session.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
