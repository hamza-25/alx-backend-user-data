#!/usr/bin/env python3
"""define module db auth
"""
from .session_exp_auth import SessionExpAuth
from datetime import datetime
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """define SessionDBAuth class
    """
    def create_session(self, user_id=None) -> str:
        """cretae session id from SessionDBAuth
        """
        session_id = super().create_session(user_id)
        if not isinstance(session_id, str):
            return None
        session_items = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        session_user = UserSession(session_items)
        session_user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """returns the User ID by requesting UserSession
        """
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None) -> bool:
        """delete session id
        """
        return super().destroy_session(request)
