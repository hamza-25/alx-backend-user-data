#!/usr/bin/env python3
"""End-to-end integration test Module
"""
import requests
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
host = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """
    """
    end_point = '/users'
    full_url = f'{host}{end_point}'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(full_url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(full_url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    """
    end_point = '/sessions'
    full_url = f'{host}{end_point}'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(full_url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    """
    end_point = '/sessions'
    full_url = f'{host}{end_point}'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(full_url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    """
    end_point = '/profile'
    full_url = f'{host}{end_point}'
    response = requests.get(full_url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    """
    end_point = '/profile'
    full_url = f'{host}{end_point}'
    data = {
        'session_id': session_id,
    }
    response = requests.get(full_url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    """
    end_point = '/sessions'
    full_url = f'{host}{end_point}'
    data = {
        'session_id': session_id,
    }
    response = requests.delete(full_url, data=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    """
    end_point = '/reset_password'
    full_url = f'{host}{end_point}'
    data = {'email': email}
    response = requests.post(full_url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    assert "reset_token" in response.json()
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    """
    end_point = '/reset_password'
    full_url = f'{host}{end_point}'
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    presonse = requests.put(full_url, data=body)
    assert presonse.status_code == 200
    assert presonse.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
