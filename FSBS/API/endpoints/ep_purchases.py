from sqlalchemy.orm import Session
from FSBS.API.structures import schemas
from FSBS.API.database import database_interface as dbi
from FSBS.API.dependencies import get_db

# Create an endpoint router
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix='/api/purchases',
    tags=['Purchases'],
    dependencies=[Depends(get_db)]
)


@router.get(
    path='/{purchase_id}/',
    summary='Get single purchase')
def undef2():
    raise NotImplementedError()


@router.get(
    path='/',
    summary='Get all purchases')
def undef1():
    raise NotImplementedError()


@router.post(
    path='/',
    summary='Post new purchase')
def post_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    raise NotImplementedError()


@router.post(
    path='/batch',
    summary='Post multiple new purchases')
def undef4():
    raise NotImplementedError()


@router.patch(
    path='/{purchase_id}',
    summary='Modify single purchase')
def undef7():
    raise NotImplementedError()


@router.patch(
    path='/',
    summary='Modify multiple purchases')
def undef8():
    raise NotImplementedError()


@router.delete(
    path='/{purchase_id}',
    summary='Delete single purchase')
def undef5():
    raise NotImplementedError()


@router.delete(
    path='/batch',
    summary='Delete multiple purchases')
def undef6():
    raise NotImplementedError()
