#!/usr/bin/env python3
"""
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def hanlde_all_session():
    """login with session
    """
    email = request.form.get('email')
    password = request.form.get('email')
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    valid_pass = User.is_valid_password(password)
    if not valid_pass:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(getattr(users[0], 'id'))
    response = jsonify(users[0].to_json())
    response.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE session logout
    """
    from api.v1.app import auth
    deleted = auth.destroy_session(request)
    if not deleted:
        abort(404)
    return jsonify({})
