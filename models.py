from sqlalchemy import Column, Integer, String, Float, BigInteger
from database import Base

# models.py ichida
# models.py
class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, index=True) # BigInteger bo'lishi shart!
    full_name = Column(String)
    phone = Column(String)




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





