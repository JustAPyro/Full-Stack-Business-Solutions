from sqlalchemy.orm import Session
from FSBS.API.structures import schemas, models
import datetime

from FSBS.API.dependencies import bcrypt, oauth2_scheme


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        password=bcrypt.generate_password_hash(user.password, 4).decode('UTF-8'),  # TODO: Hook this up to config
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        date_registered=datetime.datetime.now(),
        date_last_active=datetime.datetime.now())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def create_purchase(db: Session, purchase: schemas.PurchaseCreate, user_id: int):

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

