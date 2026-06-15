from functools import wraps
from flask import session
from flask import redirect
from flask import url_for


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            return redirect(
                url_for("auth.login")
            )

        return func(*args, **kwargs)

    return wrapper


def role_required(role):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if "role" not in session:

                return redirect(
                    url_for("auth.login")
                )

            if session["role"] != role:

                return "Access Denied", 403

            return func(*args, **kwargs)

        return wrapper

    return decorator