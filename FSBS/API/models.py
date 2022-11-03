import jwt
from extensions import db, bcrypt
from secrets import secrets
import datetime


class User(db.Model):
    __tablename__ = 'users'

    # Primary key user ID
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Username and password fields
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    # Contact info
    phone = db.Column(db.String(10), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)

    # Activity information
    date_registered = db.Column(db.DateTime, nullable=False)
    date_last_active = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password, phone=None, email=None):
        # Record username and then encrypt/hash and record password
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password,
            4  # TODO: Hook this up to config
        ).decode('UTF-8')

        # Assign contact info (If available, otherwise default to None)
        self.phone = phone
        self.email = email

        # Record the register date and also set "now" to last activity
        self.date_registered = datetime.datetime.now()
        self.date_last_active = datetime.datetime.now()

    @staticmethod
    def validate(username, password, phone=None, email=None):
        if db.session.query(db.exists().where(User.username == username)).scalar():
            return False  # Username already exists
        return True

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
