from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session
import database, models, schemas

app = FastAPI()

# Baza jadvalini yaratish (agar kerak bo'lsa)
models.Base.metadata.create_all(bind=database.engine)

@app.post("/trees", response_model=schemas.Tree)
def create_tree(tree: schemas.Tree, db: Session = Depends(database.get_db)):
    db_tree = models.Tree(**tree.dict())
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)
    return db_tree

@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user
import requests

import database 
import models
import schemas
from database import SessionLocal, engine, Base


BOT_TOKEN = "8565818987:AAEciIAbwHVGjkuJ7TwwdCfKjKlXYj8annI"



# Database table yaratish
models.Base.metadata.create_all(bind=database.engine)

@app.post("/trees", response_model=schemas.Tree)
def create_tree(tree: schemas.Tree, db: Session = Depends(database.get_db)):
    db_tree = models.Tree(**tree.dict())
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)
    return db_tree

@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user
# Foydalanuvchini ro'yxatdan o'tkazish (Daraxt yuborganda chaqiriladi)
@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user:
        return db_user
    new_user = models.User(user_id=user.user_id, user_name=user.user_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# To'lov ma'lumotlarini yangilash (Botdagi PaymentForm uchun)
@app.post("/update_payment")
def update_payment(data: schemas.PaymentUpdate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    
    if data.card: user.card = data.card
    if data.phone_pay: user.phone_pay = data.phone_pay
    
    db.commit()
    return {"message": "Ma'lumotlar yangilandi"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# API ENDPOINTS
# -----------------------------

@app.post("/trees/")
def create_tree(tree: schemas.Tree, db: Session = Depends(get_db)):
    return crud.create_tree(db, tree)


@app.get("/trees/")
def get_trees(db: Session = Depends(get_db)):
    return crud.get_trees(db)


# -----------------------------
# TELEGRAM PHOTO PROXY
# -----------------------------

@app.get("/photo/{file_id}")
def get_photo(file_id: str):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    r = requests.get(url).json()

    file_path = r["result"]["file_path"]

    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    img = requests.get(file_url)

    return Response(content=img.content, media_type="image/jpeg")


# -----------------------------
# DASHBOARD
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def dashboard():

    return """
<!DOCTYPE html>
<html>
<head>

<title>GreenPay Dashboard</title>

<style>

body{
font-family:Arial;
background:#f4f4f4;
}

.card{
background:white;
padding:15px;
margin:10px;
border-radius:10px;
box-shadow:0 0 5px rgba(0,0,0,0.2);
width:300px;
display:inline-block;
vertical-align:top;
}

img{
width:100%;
border-radius:8px;
}

button{
padding:10px 15px;
font-size:16px;
margin:10px;
}

</style>

</head>

<body>

<h1>🌳 GreenPay Dashboard</h1>

<button onclick="loadTrees()">Daraxtlarni yuklash</button>

<div id="trees"></div>

<script>

async function loadTrees(){

const res = await fetch('/trees/')
const data = await res.json()

let html = ""

data.forEach(tree => {

html += `
<div class="card">

<b>User:</b> ${tree.user_name}<br>
<b>Telefon:</b> ${tree.phone}<br>
<b>Daraxt:</b> ${tree.tree_type}<br><br>

<img src="/photo/${tree.photo}">

<br><br>

<a href="https://maps.google.com/?q=${tree.latitude},${tree.longitude}" target="_blank">
📍 Xarita
</a>

</div>
`

})

document.getElementById("trees").innerHTML = html

}

</script>

</body>
</html>
"""






