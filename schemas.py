from pydantic import BaseModel

class TreeCreate(BaseModel):
    user_id: int
    user_name: str
    tree_type: str
    location: str   # 🔥 SHU YO‘Q EDI
    latitude: float
    longitude: float


class FinanceCreate(BaseModel):
    type: str
    amount: float
    description: str

