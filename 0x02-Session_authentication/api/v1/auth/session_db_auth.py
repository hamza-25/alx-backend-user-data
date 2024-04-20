#!/usr/bin/env python3
"""define module db auth
"""
from .session_auth import SessionAuth
from .session_exp_auth import SessionExpAuth
import os
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """define SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """cretae session id from SessionDBAuth
        """
        return super().create_session(user_id)

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession
        """
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """delete session id
        """
        return super().destroy_session(request)
