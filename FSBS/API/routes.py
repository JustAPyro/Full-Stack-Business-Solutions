import json
from extensions import bcrypt
from flask import request, Response
from extensions import db
from models import User, Transaction


def hello():
    return '{"message": "Hello world!"}'


def create_user():
    return request.form.get('username')


def transaction_post():
    # Start by trying to get the requesting user
    user = User.get_user(request)

    print(user)
    # If the user couldn't be validated return an error
    if not user:
        return "ERROR"

    # Unpack the rest of the information from the request
    location = request.form.get('location')
    cost = request.form.get('cost')
    tax = request.form.get('tax')
    purchase_time = request.form.get('purchase_time')

    # Create a transaction
    transaction = Transaction(user.user_id,
                              location=location,
                              cost=cost,
                              tax=tax,
                              purchase_time=purchase_time)

    # Insert the transaction in the database
    db.session.add(transaction)
    db.session.commit()

    return Response(
        response="Success",
        status=200,
        content_type='JSON')


def authorize_user():
    # Collect data
    print("hit")
    data = request.get_json()

    if not data:
        return Response(
            response=json.dumps({
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"}),
            status=400,
            content_type='JSON')

    email = data['email']
    password = data['password']
    print('found data')
    # Find the user in the database
    user = User.query.filter_by(email=email).first()
    print('found user')

    if user and bcrypt.check_password_hash(user.password, password):
        print('bcrypt in')
        auth_token = user.encode_auth_token(user.user_id)
        print('token gen')
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
        response=json.dumps({'ERROR': "ERROR"}),
        status=401,
        content_type='JSON')


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
