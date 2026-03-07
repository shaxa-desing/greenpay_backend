from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    user_id: int
    user_name: str
    username: Optional[str] = None
    phone: str

class Tree(BaseModel):
    user_id: int
    user_name: str # Dashboardda null chiqmasligi uchun shart
    phone: str
    tree_type: str
    latitude: float
    longitude: float
    photo: str
    
class PaymentUpdate(BaseModel):
    user_id: int
    card: Optional[str] = None
    phone_pay: Optional[str] = None

    class Config:
        from_attributes = True


