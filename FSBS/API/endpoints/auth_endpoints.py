import json
from flask import request, Response

from FSBS.API.extensions import db, bcrypt
from FSBS.API.database.models import User, Transaction
from FSBS.API.responses import errors
from FSBS.API.database import validation


def authorize_user():
    # Collect data
    data = request.get_json()

    if not data:
        return errors.MISSING_BODY()

    email = data['email']
    password = data['password']

    # Process the email by forcing it to lower
    email = email.lower()

    # Find the user in the database
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):

        # get the token
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
        response=json.dumps({'ERROR': "User could not be found."}),
        status=401,
        content_type='JSON')


def register_user():
    # Collect
    data = request.get_json()

    if not data:
        return errors.MISSING_BODY(data={})

    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']

    valid, issues = User.validator(email, password, first_name, last_name, phone, data=data)
    if not valid: return errors.MALFORMED_BODY(issues=issues, data={}, request=request)

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
