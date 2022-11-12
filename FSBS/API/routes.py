import json

from FSBS.API.extensions import bcrypt, db
from flask import request, Response
from FSBS.API.models import User, Transaction
from FSBS.API.endpoints.transaction_endpoints import (
    transaction_endpoint,
    transactions_endpoint)
from FSBS.API.endpoints.auth_endpoints import *


def hello():
    return '{"message": "Hello world!"}'


def create_user():
    return request.form.get('username')


def register_urls(api):
    api.add_url_rule('/', methods=['GET', 'POST'], view_func=hello)
    api.add_url_rule('/register', methods=['POST'], view_func=register_user)
    api.add_url_rule('/authorize', methods=['POST'], view_func=authorize_user)
    api.add_url_rule('/transaction', methods=['GET', 'POST'], view_func=transaction_endpoint)
    api.add_url_rule('/transactions', methods=['GET', 'POST'], view_func=transactions_endpoint)


def register_user():
    # Collect
    data = request.get_json()
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']

    # Validate data
    validation_errors = User.validator(email, password, first_name, last_name, phone)
    if len(validation_errors) > 0:
        return Response(
            response=json.dumps(validation_errors),
            status=409,
            content_type='JSON')

    # Create new user
    user = User(email, password, first_name, last_name, phone)

    # Push to database
    db.session.add(user)
    db.session.commit()

    # Return the json representation of the user and 200 OKAY status code
    return Response(
        response=user.to_json(),
        status=200,
        content_type='JSON')
