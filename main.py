from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from fastapi import UploadFile, File, Form
import shutil
import os
import models
import schemas
import crud

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===== TELEGRAM DATA =====
@app.post("/trees/")
async def create_tree(
    user_id: int = Form(...),
    user_name: str = Form(...),
    tree_type: str = Form(...),
    location: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = file_path

    db_tree = models.Tree(
        user_id=user_id,
        user_name=user_name,
        tree_type=tree_type,
        location=location,
        latitude=latitude,
        longitude=longitude,
        image_url=image_url,
        status="pending"
    )

    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)

    return {"message": "Saved"}

# ===== BARCHA DARAxtLAR =====
@app.get("/trees/")
def get_trees(db: Session = Depends(get_db)):
    return db.query(models.Tree).all()

# ===== FINANCE =====
@app.post("/finance/")
def create_finance(fin: schemas.FinanceCreate, db: Session = Depends(get_db)):
    db_fin = models.Finance(**fin.dict())
    db.add(db_fin)
    db.commit()
    return db_fin

# ===== TASDIQLASH =====
@app.put("/trees/{tree_id}/approve")
def approve_tree(tree_id: int, db: Session = Depends(get_db)):
    tree = db.query(models.Tree).filter(models.Tree.id == tree_id).first()
    if not tree:
        return {"error": "Not found"}

    tree.status = "approved"
    db.commit()
    return {"message": "Approved"}


# ===== RAD ETISH =====
@app.put("/trees/{tree_id}/reject")
def reject_tree(tree_id: int, db: Session = Depends(get_db)):
    tree = db.query(models.Tree).filter(models.Tree.id == tree_id).first()
    if not tree:
        return {"error": "Not found"}

    tree.status = "rejected"
    db.commit()
    return {"message": "Rejected"}


@app.get("/finance/")
def get_finance(db: Session = Depends(get_db)):
    return db.query(models.Finance).all()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")








