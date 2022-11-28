import os
from typing import Optional, Any

import jwt
import json
from flask import request, Response
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from FSBS.API.extensions import db, bcrypt
import datetime

from FSBS.API.responses import errors


class User(db.Model):
    __tablename__ = 'users'

    # Primary key user ID and email which acts as username
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Password field
    password = db.Column(db.String(255), unique=False, nullable=False)

    # User information
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=True)

    # Activity information
    date_registered = db.Column(db.DateTime, nullable=False)
    date_last_active = db.Column(db.DateTime, nullable=False)

    transactions = relationship("Transaction", back_populates="user")

    def __init__(self, email, password, first_name, last_name, phone=None):
        # Record email (Used a username)
        self.email = email

        # Hash the password and record it
        self.password = bcrypt.generate_password_hash(
            password,
            4  # TODO: Hook this up to config
        ).decode('UTF-8')

        # Assign user info
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

        # Record the register date and also set "now" to last activity
        self.date_registered = datetime.datetime.now()
        self.date_last_active = datetime.datetime.now()

    @staticmethod
    def validator(email, password, first_name, last_name, phone=None, data=None):

        # flag for valid
        valid = True

        # Map to store the issues in
        validation_errors = dict()
        validation_errors['missing'] = list()

        # Check to make sure all the required features exist
        for feature in ['email', 'password', 'first_name', 'last_name']:
            if not data[feature]: validation_errors['missing'].append(feature); valid = False

        # If the email already exists
        if db.session.query(db.exists().where(User.email == data['email'])).scalar():
            validation_errors['exists'] = ['email'];
            valid = False

        return valid, validation_errors

    def to_json(self):
        return json.dumps({
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'date_registered': self.date_registered.strftime('%m/%d/%Y'),
            'date_last_active': self.date_last_active.strftime('%m/%d/%Y')
        })

    @staticmethod
    def get_user(http_request: request) -> tuple[bool, Any, Optional[Response]]:

        # Get the header from the request
        auth_token = http_request.headers.get('Authorization')

        if not auth_token:
            return False, None, errors.MISSING_AUTH(request.json)

        # If we found a token, attempt to decode it
        token = User.decode_auth_token(auth_token)

        if token == 'EXPIRED':  # If token timed out / expired return error
            return False, None, errors.EXPIRED_AUTH(request.json)

        if token == 'INVALID':  # If token was invalid pass up the appropriate error
            return False, None, errors.INVALID_AUTH()

        user = User.query.filter_by(user_id=token).first()

        if not user:  # If user wasn't found return an appropriate error
            return False, None, errors.USER_NOT_FOUND(user_id=token, data=request.json)

        return True, user, None

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :param user_id:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key=os.environ.get("AUTH_KEY_SECRET", "Default"),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.environ.get("AUTH_KEY_SECRET", "default_val"), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'EXPIRED'
        except jwt.InvalidTokenError:
            return 'INVALID'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    # The transaction_id and the user_id of the owner
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), unique=False, nullable=False)
    user = relationship('User', back_populates='transactions')

    # Store the location of the transaction
    location = db.Column(db.String(255), unique=False, nullable=False)

    # Store the cost and tax of the transaction
    cost = db.Column(db.Integer, unique=False, nullable=False)
    tax = db.Column(db.Integer, unique=False, nullable=False)

    # Save the time of the purchase
    purchase_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, location, cost, tax, purchase_time=None):
        self.user_id = user_id
        self.location = location
        self.cost = cost
        self.tax = tax

        # If the caller provides a date use that, otherwise use now
        if purchase_time:
            m, d, y = purchase_time.split('/')
            self.purchase_time = datetime.datetime(year=int(y), month=int(m), day=int(d))
        else:
            self.purchase_time = datetime.datetime.now()

    @staticmethod
    def validator(location, cost, tax, purchase_time):

        # flag for valid
        valid = True

        # Map to store the issues in
        validation_errors = dict()
        validation_errors['missing'] = list()

        if not location:
            valid = False
            validation_errors['missing'].append('location')
        if not cost:
            valid = False
            validation_errors['missing'].append('cost')
        if not tax:
            valid = False
            validation_errors['missing'].append('tax')

        return valid, validation_errors

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'transaction_id': self.transaction_id,
            'location': self.location,
            'cost': self.cost,
            'tax': self.tax
        }

    def to_json(self):
        return json.dumps(self.to_dict())
