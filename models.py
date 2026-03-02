from sqlalchemy import Column, Integer, String, Float
from database import Base

class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True, index=True)
    tree_type = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    user_name = Column(String)
    user_id = Column(Integer)
    status = Column(String, default="pending")
