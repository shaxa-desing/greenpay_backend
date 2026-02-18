from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# ===== TELEGRAM DATA =====
@app.post("/trees/")
def create_tree(tree: schemas.TreeCreate, db: Session = Depends(get_db)):
    db_tree = models.Tree(**tree.dict())
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)
    return db_tree

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


