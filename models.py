from sqlalchemy import Column, Integer, String, Float, BigInteger

class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    user_name = Column(String)
    tree_type = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String)   # ⬅ YANGI
    status = Column(String, default="pending")
