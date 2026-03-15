from sqlalchemy import Column, Integer, String, Float, BigInteger
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True)
    full_name = Column(String)
    phone = Column(String)
    card = Column(String, nullable=True)
    balance = Column(Integer, default=0)

class Tree(Base):
    __tablename__ = "trees"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    user_name = Column(String)
    category = Column(String) # Mevali yoki Manzarali
    tree_type = Column(String) # Olma, Gilos va h.k.
    latitude = Column(Float)
    longitude = Column(Float)
    photo = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected
    price = Column(Integer, default=0)
