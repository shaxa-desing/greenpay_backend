from sqlalchemy import Column, Integer, String, Float, BigInteger
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    full_name = Column(String)
    username = Column(String, nullable=True) # <-- Shu qatorni qo'shing
    phone = Column(String, nullable=True)
    card = Column(String, nullable=True)     # <-- Karta uchun joy




class Tree(Base):
    __tablename__ = "trees"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    user_name = Column(String)
    tree_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    photo = Column(String)
    status = Column(String, default="pending") # Tasdiqlash uchun







