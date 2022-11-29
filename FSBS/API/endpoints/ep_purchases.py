from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from FSBS.API.structures import schemas
from FSBS.API.database import database_interface as dbi
from FSBS.API.dependencies import get_db, get_current_user
from FSBS.API.structures.schemas import User

router = APIRouter(
    prefix='/api/purchases',
    tags=['Purchases'],
    dependencies=[Depends(get_db)]
)


@router.get(
    path='/{purchase_id}/',
    summary='Get single purchase')
def get_purchase_single(purchase_id: int,
                        db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    return dbi.get_purchase_by_id_with_user(db, purchase_id=purchase_id, user_id=user.user_id)


@router.get(
    path='/',
    summary='Get all purchases')
def undef1():
    raise NotImplementedError()


@router.post(
    path='/',
    summary='Post new purchase')
def post_purchase_single(purchase: schemas.PurchaseCreate,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    return dbi.create_purchase(db=db, purchase=purchase, user_id=user.user_id)


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
