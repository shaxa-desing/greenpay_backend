from pydantic import BaseModel

class Tree(BaseModel):
    user_id: int
    user_name: str
    phone: str
    tree_type: str
    latitude: float
    longitude: float
    photo: str

    class Config:
        orm_mode = True
