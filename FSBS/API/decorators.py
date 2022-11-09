import json
from functools import wraps

from flask import request

from models import User
from server_util import construct_error_response


def user_endpoint(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = User.get_user(request)

        if not user:
            return construct_error_response(400, json.dumps({'ERRORS': 'Could not find user'}))

        return f(user, *args, **kwargs)

    return decorator
