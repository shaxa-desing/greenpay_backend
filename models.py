from sqlalchemy import Column, Integer, String, Float, BigInteger
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    full_name = Column(String)
    username = Column(String, nullable=True) # <-- Shu qatorni qo'shing
    phone = Column(String, nullable=True)
    card = Column(String, nullable=True)     # <-- Karta uchun joy




class TreeCreate(BaseModel):
    user_id: int
    user_name: str # Modelsda user_name bor
    tree_type: str
    latitude: float
    longitude: float
    photo: str # Bu yerda Telegram file_id saqlanadi
    status = Column(String, default="pending") # Tasdiqlash uchun





