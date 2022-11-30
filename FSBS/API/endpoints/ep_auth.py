from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from FSBS.API.dependencies import get_db
from FSBS.API.structures.schemas import Token
from FSBS.API.utility.auth import create_access_token
from FSBS.API.database import database_interface as dbi
from FSBS.API.utility.auth import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix='/api/auth',
    tags=['Authorization'],
    dependencies=[Depends(get_db)]
)


@router.post('/token', response_model=Token)
async def post_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Get the user with our auth method
    user = dbi.authenticate_user(db, form_data.username.lower(), form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email} ,
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

