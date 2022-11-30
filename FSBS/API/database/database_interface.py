from sqlalchemy.orm import Session
from FSBS.API.structures import schemas, models
from FSBS.API.utility.auth import get_password_hash, verify_password
import datetime


def submit_request(db: Session, request: schemas.APIRequestCreate):
    db_api_request = models.APIRequest(**request.dict())
    db.add(db_api_request)
    db.commit()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email.lower(),
        password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        date_registered=datetime.datetime.now(),
        date_last_active=datetime.datetime.now())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    # Get the user based on username (email)
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def create_purchases(db: Session, purchase: schemas.PurchaseCreate, user_id: int):
    # *if* time wasn't included, set it to now
    if purchase.purchase_time is None:
        purchase.purchase_time = datetime.datetime.now()

    # Create a db purchase model by unpacking the passed purchase item
    db_purchase = models.Purchase(**purchase.dict(), user_id=user_id)

    # Commit to db and return it
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_purchase_by_id_with_user(db: Session, purchase_id: int, user_id: int):
    return (db.query(models.Purchase)
            .filter(models.Purchase.purchase_id == purchase_id)
            .filter(models.Purchase.user_id == user_id)
            .first())


def delete_purchase_by_id_with_user(db: Session, purchase_id: int, user_id: int) -> bool:
    # First search db for a purchase with this id and user id
    purchase = (db.query(models.Purchase)
                .filter(models.Purchase.purchase_id == purchase_id)
                .filter(models.Purchase.user_id == user_id)
                .first())

    # If we didn't find this purchase return false
    if not purchase:
        return False

    # Otherwise delete it and return true
    db.delete(purchase)
    db.commit()
    return True
