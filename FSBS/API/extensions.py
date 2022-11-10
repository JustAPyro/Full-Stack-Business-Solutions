from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Establish SQLAlchemy Database extension
db = SQLAlchemy()

# Establish Bcrypt extension for hashing passwords
bcrypt = Bcrypt()
