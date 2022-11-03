import json
from extensions import bcrypt
from flask import request, Response
from extensions import db
from models import User


def names():
    return '{"name": "Luke", "last": "Hanna", "dob": "10/02/1997"}'


def create_user():
    return request.form.get('username')


def transaction_post():





def authorize_user():
    # Collect data
    email = request.form.get('email')
    password = request.form.get('password')

    # Find the user in the database
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        auth_token = user.encode_auth_token(user.user_id)
        if auth_token:
            return Response(
                response=json.dumps({'auth_token': auth_token}),
                status=200,
                content_type='JSON')
        else:
            return Response(
                response=json.dumps({'ERROR': 'User does not exist.'}),
                status=404,
                content_type='JSON')

    return Response(  # TODO: Add a better response here
        response=json.dumps({'FAIL': "ERROR"}),
        status=401,
        content_type='JSON')


def register_user():
    # Collect Data
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')

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
