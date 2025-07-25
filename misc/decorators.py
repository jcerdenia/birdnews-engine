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


def require_auth(config):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_token = request.headers.get("X-API-TOKEN")

            if not api_token or api_token != config.API_TOKEN:
                abort(401)  # Unauthorized

            return f(*args, **kwargs)

        return decorated_function

    return decorator
