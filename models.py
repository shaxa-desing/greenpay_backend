from sqlalchemy import Column, Integer, String, Float
from database import Base

class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_name = Column(String)
    tree_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String, default="pending")


class Finance(Base):
    __tablename__ = "finance"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # income / expense
    amount = Column(Float)
    description = Column(String)
