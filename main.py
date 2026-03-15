import os
import sys
import requests
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse # FileResponse qo'shildi
from fastapi.staticfiles import StaticFiles # StaticFiles qo'shildi

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import models
import schemas
import database

app = FastAPI(title="GreenPay API")

# Statik fayllarni serverga ulash (HTML, CSS, JS shu yerda bo'ladi)
app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=database.engine)

BOT_TOKEN = "8565818987:AAFtp_uIUnZOdeqLRjWP2E_2eObcEFLJ28o" 

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Foydalanuvchi mavjudligini tekshirish

@app.get("/", response_class=FileResponse)
async def read_index():
    return "static/index.html"

@app.post("/users/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        user_id=user.user_id,
        full_name=user.full_name,
        phone=user.phone,
        balance=0
    )
    db.add(new_user)
    db.commit()
    return {"status": "ok"}

@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return user

@app.post("/update-card/{user_id}")
def update_card(user_id: int, data: schemas.CardUpdateSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404)
    user.card = data.card
    user.phone = data.phone
    db.commit()
    return {"status": "success"}

@app.get("/trees/")
def get_all_trees(db: Session = Depends(get_db)):
    trees = db.query(models.Tree).all()
    return trees

@app.post("/trees/")
def create_tree(tree: schemas.TreeCreate, db: Session = Depends(get_db)):
    new_tree = models.Tree(
        user_id=tree.user_id,
        user_name=tree.user_name,
        category=tree.category,
        tree_type=tree.tree_type,
        latitude=tree.latitude,
        longitude=tree.longitude,
        photo=tree.photo,
        price=tree.price,
        status="pending"
    )
    db.add(new_tree)
    db.commit()
    db.refresh(new_tree)
    return {"message": "Success", "tree_id": new_tree.id}

# Admin qabul qilganda ishlaydi
@app.post("/trees/approve/{tree_id}")
def approve_tree(tree_id: int, db: Session = Depends(get_db)):
    tree = db.query(models.Tree).filter(models.Tree.id == tree_id).first()
    if not tree or tree.status != "pending":
        return {"status": "error"}
    
    tree.status = "approved"
    user = db.query(models.User).filter(models.User.user_id == tree.user_id).first()
    if user:
        user.balance += tree.price # Hisobiga pul tushadi
    db.commit()
    return {"status": "success"}

# Admin rad etganda ishlaydi
@app.post("/trees/reject/{tree_id}")
def reject_tree(tree_id: int, db: Session = Depends(get_db)):
    tree = db.query(models.Tree).filter(models.Tree.id == tree_id).first()
    if tree:
        tree.status = "rejected"
        db.commit()
    return {"status": "success"}
