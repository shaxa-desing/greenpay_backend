# schemas.py
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    user_id: int
    user_name: Optional[str] = None  # Majburiy emas qilib qo'yamiz
    full_name: Optional[str] = None  # Botdan kelishi ehtimoli bo'lgan maydon
    username: Optional[str] = None
    phone: Optional[str] = None

class CardUpdateSchema(BaseModel):
    card: str
    phone: str

class TreeCreate(BaseModel):
    user_id: int
    user_name: str
    phone: Optional[str] = None
    tree_type: str
    latitude: float
    longitude: float
    photo: str


