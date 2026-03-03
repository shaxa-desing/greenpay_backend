from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

trees = []

@app.get("/")
def root():
    return {"status":"working"}

@app.get("/trees/")
def get_trees():
    return trees

@app.post("/trees/")
async def create_tree(
    user_id: int = Form(...),
    user_name: str = Form(...),
    tree_type: str = Form(...),
    location: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    file: UploadFile = File(...)
):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    tree_data = {
        "user_id": user_id,
        "user_name": user_name,
        "tree_type": tree_type,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "image_url": f"/uploads/{file.filename}"
    }

    trees.append(tree_data)

    return {"message":"saved"}
