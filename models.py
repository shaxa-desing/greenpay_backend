from sqlalchemy import Column, Integer, String, Float
from database import Base

# Daraxtlar uchun model (mavjud)
class Tree(Base):
    __tablename__ = "trees"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_name = Column(String)
    phone = Column(String)
    tree_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    photo = Column(String)

# YANGI: Foydalanuvchilar uchun model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True) # Telegram ID
    full_name = Column(String)
    card = Column(String, nullable=True)
    phone_pay = Column(String, nullable=True)
