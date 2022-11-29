from sqlalchemy.orm import Session
from FSBS.API.structures import schemas
from FSBS.API.database import database_interface as dbi
from FSBS.API.dependencies import get_db

# Create an endpoint router
from fastapi import APIRouter, Depends
router = APIRouter(
    prefix='/api/users',
    tags=['Users'],
    dependencies=[Depends(get_db)]
)


@router.post('/', response_model=schemas.User)
def post_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return dbi.create_user(db=db, user=user)


@router.get('/{user_id}/', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = dbi.get_user(db, user_id=user_id)
    return db_user

@router.delete('/{user_id}/', response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    dbi.delete_user(db, user_id=user_id)
    return 'lol'



