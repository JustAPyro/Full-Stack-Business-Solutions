from flask import request
from extensions import db
from models import User


def names():
    return '{"name": "Luke", "last": "Hanna", "dob": "10/02/1997"}'


def create_user():
    return request.form.get('username')


def register_user():
    # Collect Data
    username = request.form.get('username')
    password = request.form.get('password')

    print(f"Trying to create user {username}")

    if not (User.validate(username, password)):
        return "Can't create that user!"

    # Create new user
    u = User(username, password)
    User.validate(username, password)
    db.session.add(u)
    db.session.commit()

    return "Created!"
