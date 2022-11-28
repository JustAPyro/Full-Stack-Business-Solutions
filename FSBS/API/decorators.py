from flask import request

from FSBS.API.models import User


def user_endpoint(func):
    def wrapper(*args, **kwargs):

        # Start by trying to get the requesting user
        success, user, error_response = User.get_user(request)

        # If the user couldn't be validated return an error
        if not success:
            return error_response

        # Return the function called with the user
        f = func(user, *args, **kwargs)

        return f
    return wrapper
