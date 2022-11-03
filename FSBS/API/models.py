from extensions import db, bcrypt
import datetime


class User(db.Model):
    __tablename__ = 'users'

    # Primary key user ID
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Username and password fields
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

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
