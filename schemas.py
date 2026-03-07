from pydantic import BaseModel
from typing import Optional

class Tree(BaseModel):
    user_id: int
    tree_type: str
    latitude: float
    longitude: float
    photo: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    user_id: int
    user_name: str
    
class PaymentUpdate(BaseModel):
    user_id: int
    card: Optional[str] = None
    phone_pay: Optional[str] = None

    class Config:
        from_attributes = True

