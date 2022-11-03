import jwt
import json
from sqlalchemy import ForeignKey
from extensions import db, bcrypt
from secrets import secrets
import datetime


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
    def validator(email, password, first_name, last_name, phone=None):
        # Map to store the errors in
        errors = []

        if db.session.query(db.exists().where(User.email == email)).scalar():
            errors.append({'EMAIL_EXISTS_ERROR': email})

        return errors

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
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :param user_id:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                secrets['secret_key'],
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
            payload = jwt.decode(auth_token, secrets['secret_key'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    # The transaction_id and the user_id of the owner
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), unique=False, nullable=False)

    # Store the location of the transaction
    location = db.Column(db.String(255), unique=False, nullable=False)

    # Store the cost and tax of the transaction
    cost = db.Column(db.Integer, unique=False, nullable=False)
    tax = db.Column(db.Integer, unique=False, nullable=False)

    # Save the time of the purchase
    purchase_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, location, cost, tax):
        self.user_id = user_id
        self.location = location
        self.cost = cost
        self.tax = tax
        self.purchase_time = datetime.datetime.now()
