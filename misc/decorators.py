import os
from functools import wraps

from flask import abort, request


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None

    return wrapper


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        print(auth.username, auth.password)
        if (
            not auth
            or auth.username != os.getenv("USERNAME")
            or auth.password != os.getenv("PASSWORD")
        ):
            abort(401)  # Unauthorized

        return f(*args, **kwargs)

    return decorated_function
