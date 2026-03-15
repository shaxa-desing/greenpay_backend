from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    user_id: int
    full_name: str
    phone: str

class CardUpdateSchema(BaseModel):
    card: str
    phone: str

class TreeCreate(BaseModel):
    user_id: int
    user_name: str
    category: str
    tree_type: str
    latitude: float
    longitude: float
    photo: str
    price: int
