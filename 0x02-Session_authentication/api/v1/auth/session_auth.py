#!/usr/bin/env python3
"""Define SessionAuth  Module
"""
from .auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """Define SessionAuth class
    """
    pass
