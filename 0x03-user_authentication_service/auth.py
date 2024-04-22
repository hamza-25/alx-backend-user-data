#!/usr/bin/env python3
"""Define Auth Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
