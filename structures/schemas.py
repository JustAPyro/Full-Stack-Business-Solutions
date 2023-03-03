from typing import Optional, Union
from pydantic import BaseModel
import datetime


class Token(BaseModel):
    username: str
    user_id: int
    access_token: str
    token_type: str