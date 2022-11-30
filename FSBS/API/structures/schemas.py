from typing import Optional
from pydantic import BaseModel
import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class APIRequestCreate(BaseModel):
    user_id: Optional[int]
    method: str
    endpoint: str
    query: Optional[str]
    params: Optional[dict]
    body: Optional[dict]
    caller_ip: str
    caller_port: int
    time: datetime.datetime


class APIRequest(BaseModel):
    request_id: int


class PurchaseBase(BaseModel):
    location: str
    cost: int
    tax: int
    purchase_time: Optional[datetime.datetime]


class PurchaseCreate(PurchaseBase):
    pass


class Purchase(PurchaseBase):
    user_id: int
    purchase_id: int

    class Config:
        orm_mode = True


class PurchaseBatch(BaseModel):
    purchases: list[Purchase]


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    purchases: list[Purchase] = []
    date_registered: datetime.datetime
    date_last_active: datetime.datetime

    class Config:
        orm_mode = True
