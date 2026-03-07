from pydantic import BaseModel
from typing import Optional

# Foydalanuvchini ro'yxatdan o'tkazish uchun
class UserCreate(BaseModel):
    user_id: int
    user_name: str
    phone: str

# Daraxt ekish so'rovi uchun alohida model (tavsiya etiladi)
class TreeRequest(BaseModel):
    user_id: int
    tree_type: str
    latitude: float
    longitude: float
    photo: str

# To'lov ma'lumotlarini yangilash uchun
class PaymentUpdate(BaseModel):
    user_id: int
    card: Optional[str] = None
    phone_pay: Optional[str] = None

    class Config:
        from_attributes = True # Pydantic v2 da "orm_mode" o'rniga shu ishlatiladi


