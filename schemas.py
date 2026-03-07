# schemas.py faylining to'liq va to'g'ri ko'rinishi
from pydantic import BaseModel
from typing import Optional

# Daraxt yaratish uchun model
class Tree(BaseModel):
    user_id: int
    tree_type: str
    latitude: float
    longitude: float
    photo: str

    class Config:
        from_attributes = True

# Foydalanuvchi yaratish uchun model
class UserCreate(BaseModel):
    user_id: int
    user_name: str
    phone: str

# To'lovni yangilash uchun model
class PaymentUpdate(BaseModel):
    user_id: int
    card: Optional[str] = None
    phone_pay: Optional[str] = None

    class Config:
        from_attributes = True
