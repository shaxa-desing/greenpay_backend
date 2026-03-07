from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import database, models, schemas, crud, requests

app = FastAPI()

# Baza jadvalini yaratish
models.Base.metadata.create_all(bind=database.engine)

BOT_TOKEN = "8565818987:AAEciIAbwHVGjkuJ7TwwdCfKjKlXYj8annI"

# -----------------------------
# API ENDPOINTS
# -----------------------------

@app.post("/trees/")
def create_tree(tree: schemas.Tree, db: Session = Depends(database.get_db)):
    return crud.create_tree(db, tree)

@app.get("/trees/")
def get_trees(db: Session = Depends(database.get_db)):
    return crud.get_trees(db)

# Yangi: Foydalanuvchini ID bo'yicha olish (Shaxsiy kabinet uchun)
@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user

# Yangi: Ro'yxatdan o'tish (Slash bilan)
@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user:
        return db_user
    new_user = models.User(user_id=user.user_id, full_name=user.user_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/update_payment/")
def update_payment(data: schemas.PaymentUpdate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    if data.card: user.card = data.card
    if data.phone_pay: user.phone_pay = data.phone_pay
    db.commit()
    return {"message": "Ma'lumotlar yangilandi"}

@app.get("/photo/{file_id}")
def get_photo(file_id: str):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        r = requests.get(url).json()
        file_path = r["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        img = requests.get(file_url)
        return Response(content=img.content, media_type="image/jpeg")
    except:
        raise HTTPException(status_code=404, detail="Rasm topilmadi")
