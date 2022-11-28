import datetime
import json
import os

import jwt
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from FSBS.API.database.database import Base
from FSBS.API.extensions import bcrypt


class User(Base):
    __tablename__ = 'users'

    # Primary key user ID and email which acts as username
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)

    # Password field
    password = Column(String(255), unique=False, nullable=False)

    # User information
    first_name = Column(String(255), unique=False, nullable=False)
    last_name = Column(String(255), unique=False, nullable=False)
    phone = Column(String(255), unique=True, nullable=True)

    # Activity information
    date_registered = Column(DateTime, nullable=False)
    date_last_active = Column(DateTime, nullable=False)

    transactions = relationship("Transaction", back_populates="user")



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

    '''
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
    '''
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





class Transaction(Base):
    __tablename__ = 'transactions'

    # The transaction_id and the user_id of the owner
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), unique=False, nullable=False)
    user = relationship('User', back_populates='transactions')

    # Store the location of the transaction
    location = Column(String(255), unique=False, nullable=False)

    # Store the cost and tax of the transaction
    cost = Column(Integer, unique=False, nullable=False)
    tax = Column(Integer, unique=False, nullable=False)

    # Save the time of the purchase
    purchase_time = Column(DateTime, nullable=False)

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
