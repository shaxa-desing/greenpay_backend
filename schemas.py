from typing import Optional

class UserCreate(BaseModel):
    user_id: int
    user_name: str
    phone: str
    tree_type: str
    latitude: float
    longitude: float
    photo: str
    from pydantic import BaseModel


class PaymentUpdate(BaseModel):
    user_id: int
    card: Optional[str] = None
    phone_pay: Optional[str] = None

    class Config:
        orm_mode = True

