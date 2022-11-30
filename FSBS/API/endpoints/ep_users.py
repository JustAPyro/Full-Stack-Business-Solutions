from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from FSBS.API.middleware import track_api
from FSBS.API.structures import schemas
from FSBS.API.structures.schemas import User
from FSBS.API.database import database_interface as dbi
from FSBS.API.dependencies import get_db, get_current_user, save_api_request

router = APIRouter(
    prefix='/api/users',
    tags=['Users'],
    dependencies=[Depends(get_db)]
)


@router.post('/', response_model=schemas.User)
def post_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return dbi.create_user(db=db, user=user)


@router.get('/self/', response_model=schemas.User, dependencies=[Depends(save_api_request)])
def get_self_user(user: User = Depends(get_current_user)):
    return user


@router.delete('/{user_id}/', response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    dbi.delete_user(db, user_id=user_id)
    return 'lol'
