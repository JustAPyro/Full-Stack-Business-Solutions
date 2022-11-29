from typing import Optional
from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    date_registered: datetime.datetime
    date_last_active: datetime.datetime

    class Config:
        orm_mode = True


class PurchaseBase(BaseModel):
    user_id: int
    location: str
    cost: int
    tax: int
    purchase_time: Optional[datetime.datetime]


class PurchaseCreate(PurchaseBase):
    pass


class Purchase(PurchaseBase):
    purchase_id: int
