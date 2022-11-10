import json
from enum import Enum

from flask import Response


class Code(Enum):
    EXPIRED_AUTH = 100,
    INVALID_AUTH = 101,
    MISSING_AUTH = 102,
    MISSING_PARAM = 103,
    MISSING_BODY = 104,
    MALFORMED_BODY = 105,
    USER_NOT_FOUND = 106,
    USER_NOT_AUTHORIZED = 107


def error_response(message: str, data: dict, code: Code, status: int, content_type: str):
    return Response(
        response=json.dumps({
            'status': 'error',
            'message': message,
            'code': code,
            'data': json.dumps(data)}),
        status=status,
        content_type=content_type
    )


def MISSING_AUTH(data: dict) -> Response:
    return error_response(
        message='No authorization token found. Please include "Authentication" in header.',
        data=data,
        code=Code.MISSING_AUTH,
        status=403,
        content_type='JSON')


def EXPIRED_AUTH(data: dict) -> Response:
    return error_response(
        message='Authorization token has expired. Please re-authorize by logging in again.',
        data=data,
        code=Code.EXPIRED_AUTH,
        status=401,
        content_type='JSON')


def INVALID_AUTH(data: dict) -> Response:
    return error_response(
        message='Authorization token was invalid. Please provide a valid authorization token by logging in.',
        data=data,
        code=Code.MISSING_AUTH,
        status=401,
        content_type='JSON')


def USER_NOT_FOUND(user_id: int, data: dict) -> Response:
    # add the missing user to the data
    data['Missing user_id'] = user_id
    return error_response(
        message='Auth token was decoded but there is no user with this ID in database.',
        data=data,
        code=Code.MISSING_AUTH,
        status=404,
        content_type='JSON')


def MISSING_PARAMS(params: str | list, data: dict) -> Response:
    # Get a string representation of the missing parameters
    params_string = params if isinstance(params, str) else str(params)[1:-1].replace("'", "")

    # Add the missing parameters to the data
    data['missing params'] = params

    return error_response(
        message=f'Request missing {params_string} parameters.',
        data=data,
        code=Code.MISSING_PARAM,
        status=400,
        content_type='JSON')


def USER_NOT_AUTHORIZED(resource: str, data: dict):
    return error_response(
        message=f'User is not authorized to view this {resource}. Resource likely owned by a different user.',
        data=data,
        code=Code.USER_NOT_AUTHORIZED,
        status=401,
        content_type='JSON')


def MISSING_BODY(data: dict) -> Response:
    return error_response(
        message='Missing JSON body. Please submit request with more details.',
        data=data,
        code=Code.MISSING_BODY,
        status=403,
        content_type='JSON')


def MALFORMED_BODY(issues: dict, data: dict) -> Response:
    data['issues'] = issues

    return error_response(
        message='JSON body was malformed and failed validation. Refer to data issues for missing features.',
        data=data,
        code=Code.MALFORMED_BODY,
        status=400,
        content_type='JSON')
