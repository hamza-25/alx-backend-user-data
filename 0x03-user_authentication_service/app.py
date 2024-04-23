#!/usr/bin/env python3
"""Define app Flask
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['Get'])
def home() -> str:
    """home page
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """/users route that register user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"})
    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login function that check email and password
    """
    email = request.form.get('email')
    password = request.form.get('password')
    login = AUTH.valid_login(email, password)
    if not login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """destroy a session
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('home'))


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    """return user profil if exist
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', method=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Get reset password token
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        token = None
    if token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
