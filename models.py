from sqlalchemy import Column, Integer, String, Float
from database import Base

class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_name = Column(String)
    tree_type = Column(String)
    location = Column(String)   # 🔴 MANA SHU BO‘LISHI SHART
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String, default="pending")
