from FSBS.API.database.database import SessionLocal
from flask_bcrypt import Bcrypt

# Establish Bcrypt extension for hashing passwords
bcrypt = Bcrypt()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()