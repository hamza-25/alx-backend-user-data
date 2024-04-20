#!/usr/bin/env python3
"""Define SessionExpAuth Module
"""
from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Define SessionExpAuth class
    """
    def __init__(self):
        """initialization SessionExpAuth with session_duration default 0
        """
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        if int(os.getenv('SESSION_DURATION')):
            self.session_duration = int(os.getenv('SESSION_DURATION'))

    def create_session(self, user_id=None):
        """create session for users by id from ExpAuth
        """
        user_session_id = super().create_session(user_id)
        if not user_session_id:
            return None
        super().user_id_by_session_id[user_session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return user_session_id

    def user_id_for_session_id(self, session_id=None):
        """return user id by session_id from ExpAuth
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if session_id in None:
                return None
            if self.session_duration <= 0:
                return self.user_id_by_session_id[session_id]
            if 'created_at' not in session_dict:
                return None
            current_time = datetime.now()
            duration_time = timedelta(seconds=self.session_duration)
            exp = session_dict['created_at'] + duration_time
            if exp < current_time:
                return None
            return session_dict['user_id']

        return None
