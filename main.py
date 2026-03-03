from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trees = []

@app.get("/")
def root():
    return {"status": "working"}

@app.get("/trees/")
def get_trees():
    return trees

@app.post("/trees/")
def create_tree(
    user_id: int = Form(...),
    user_name: str = Form(...),
    tree_type: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    tree = {
        "user_id": user_id,
        "user_name": user_name,
        "tree_type": tree_type,
        "latitude": latitude,
        "longitude": longitude
    }

    trees.append(tree)
    return {"message": "saved"}
