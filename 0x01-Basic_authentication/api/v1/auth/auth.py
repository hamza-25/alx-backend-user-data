#!/usr/bin/env python3
"""Define Auth Module
"""
from typing import List, TypeVar
import re


class Auth():
    """class that handle auth
    """
    from flask import request

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check auth require
        """
        if path is None or excluded_paths is None:
            return True

        for exclusion_path in excluded_paths:
            pattern = ''
            if exclusion_path.endswith('*'):
                pattern = '{}.*'.format(exclusion_path[:-1])
            elif exclusion_path.endswith('/'):
                pattern = '{}.*'.format(exclusion_path[:-1])
            else:
                pattern = '{}.*'.format(exclusion_path)
            if re.match(pattern, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """check authorization request
        """
        if request is None:
            return None
        headers = request.headers
        if not headers or not headers["Authorization"]:
            return None
        return headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """check for current user
        """
        return None
