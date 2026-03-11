from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    # ... your fields here(BaseModel):
    user_id: int
    user_name: str
    username: Optional[str] = None
    phone: Optional[str] = None

class TreeCreate(BaseModel):
    user_id: int
    user_name: str
    phone: Optional[str] = None
    tree_type: str
    latitude: float
    longitude: float
    photo: str

