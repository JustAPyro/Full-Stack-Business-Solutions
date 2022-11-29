from fastapi import Depends
from jose import jwt, JWTError
from flask_bcrypt import Bcrypt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from structures.schemas import TokenData
from database.database import SessionLocal
from utility.auth import SECRET_KEY, ALGORITHM
from database.database_interface import get_user_by_email

# Establish Bcrypt extension for hashing passwords
bcrypt = Bcrypt()

# Oauth2 definition scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=SessionLocal(), user_email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
