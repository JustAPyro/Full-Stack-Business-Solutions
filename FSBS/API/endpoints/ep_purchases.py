from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Body, FastAPI, status, HTTPException, Query

from FSBS.API.structures import schemas
from FSBS.API.structures.schemas import User
from FSBS.API.database import database_interface as dbi
from FSBS.API.dependencies import get_db, get_current_user

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
def get_purchase_all(user: User = Depends(get_current_user)):
    return user.purchases


@router.post(
    path='/',
    summary='Post new purchase')
def post_purchase_single(purchase: schemas.PurchaseCreate,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    return dbi.create_purchases(db=db, purchase=purchase, user_id=user.user_id)


@router.post(
    path='/batch/',
    summary='Post multiple new purchases',
    response_model=list[schemas.Purchase])
def post_purchase_batch(purchases: list[schemas.PurchaseCreate],
                        db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    # Iterate through and insert each user into DB
    # TODO: If performance gets bad this could be enhanced
    db_purchase_out = []
    for purchase in purchases:
        db_purchase_out.append(dbi.create_purchases(db, purchase, user.user_id))
    return db_purchase_out


@router.patch(
    path='/{purchase_id}',
    summary='Modify single purchase')
def patch_purchase_single(purchase_id: int,
                          purchase_modification: schemas.PurchaseModify,
                          db: Session = Depends(get_db), 
                          user: User = Depends(get_current_user)):
    dbi.modify_purchase_by_id_with_user(db, purchase_id, purchase_modification, user.user_id)


@router.patch(
    path='/',
    summary='Modify multiple purchases')
def patch_purchase_multiple(purchase_modifications: dict[int, schemas.PurchaseModify],
                            db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    for p_id in purchase_modifications:
        dbi.modify_purchase_by_id_with_user(db, p_id, purchase_modifications[p_id], user.user_id)

@router.delete(
    path='/batch/',
    summary='Delete multiple purchases',
    response_model=dict[int, bool])
def delete_purchase_batch(did: list[int] | None = Query(default=None),
                          db: Session = Depends(get_db),
                          user: User = Depends(get_current_user)):
    print("fired")
    success_response = {}
    for i in did:
        success = dbi.delete_purchase_by_id_with_user(db, i, user.user_id)
        success_response[i] = success

    return success_response



@router.delete(
    path='/{purchase_id}/',
    summary='Delete single purchase')
def delete_purchase_single(purchase_id: int,
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    # Attempt to delete the requested purchase
    success = dbi.delete_purchase_by_id_with_user(db, purchase_id, user.user_id)

    # If it wasn't successful throw an error
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Purchase Resource doesn't belong to this user.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Otherwise return 204 to indicate success
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


