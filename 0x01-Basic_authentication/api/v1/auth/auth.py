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
        return False

    def authorization_header(self, request=None) -> str:
        """check authorization request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """check for current user
        """
        return None
