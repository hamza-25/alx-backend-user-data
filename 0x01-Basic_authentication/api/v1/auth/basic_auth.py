#!/usr/bin/env python3
"""Define BasicAuth Module
"""
from .auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """Define BasicAuth inherit from Auth()
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header.split(' ')[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string
        """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            b64decode(base64_authorization_header)
        except Exception:
            return None
        return b64decode(base64_authorization_header).decode('utf-8')
