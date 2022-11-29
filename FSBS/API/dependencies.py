from FSBS.API.database.database import SessionLocal
from flask_bcrypt import Bcrypt
from fastapi.security import OAuth2PasswordBearer

# Establish Bcrypt extension for hashing passwords
bcrypt = Bcrypt()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token)")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
