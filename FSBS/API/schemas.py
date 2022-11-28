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
    first_name: str
    last_name: str
    phone: str
    date_registered: datetime.datetime
    date_last_active: datetime.datetime

    class Config:
        orm_mode = True
