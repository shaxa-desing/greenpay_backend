from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

trees = []

class Tree(BaseModel):
    user_id: int
    user_name: str
    phone: str
    tree_type: str
    latitude: float
    longitude: float
    photo: str


@app.post("/trees/")
def create_tree(tree: Tree):
    trees.append(tree)
    return {"status": "saved"}


@app.get("/trees/")
def get_trees():
    return trees
