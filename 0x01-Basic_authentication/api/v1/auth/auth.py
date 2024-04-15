#!/usr/bin/env python3
"""Define Auth Module
"""
from typing import List, TypeVar


class Auth():
    """class that handle auth
    """
    from flask import request

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check auth require
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths and path[-1] == "/":
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """check authorization request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """check for current user
        """
        return None
