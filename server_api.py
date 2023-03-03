from fastapi import APIRouter, Request, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from structures.schemas import Token
from structures.exceptions import UNAUTHORIZED_EXCEPTION
from dependencies import database

# Create the router
api = APIRouter(prefix='/api')


@api.post('/auth/token/', response_model=Token, summary="Creates an authorization token", tags=['Authorization'])
async def post_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database)):
    # Get the user with our auth method
    user = dbi.authenticate_user(db, form_data.username.lower(), form_data.password)

    if not user:
        raise UNAUTHORIZED_EXCEPTION

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expires
    )

    # Use the set_cookie header in the response so the client saves the seceret
    response.set_cookie('Authorization', f'bearer {access_token}')
    return {'username': user.username, 'user_id': user.user_id, 'access_token': access_token, 'token_type': 'bearer'}