import os
import sys
import requests # API ga so'rov yuborish uchun kerak
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session # Session ni import qilish esdan chiqqan edi

# Papkani python path ga qo'shamiz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# O'zimizning fayllarni import qilamiz
import models
import schemas
import database

app = FastAPI(title="GreenPay API")

# Ma'lumotlar bazasi jadvallarini yaratish (database.engine orqali)
models.Base.metadata.create_all(bind=database.engine)

# DIQQAT: Bot tokenini shu yerga yozishni unutmang
BOT_TOKEN = "8565818987:AAFtp_uIUnZOdeqLRjWP2E_2eObcEFLJ28o" 

# Ma'lumotlar bazasi bilan xavfsiz ishlash uchun sessiya ochuvchi funksiya
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
async def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    # Modelga ma'lumotlarni to'g'ri bog'laymiz
    new_user = models.User(
        user_id=user.user_id,
        full_name=user.full_name or user.username, # Ikkalasidan birini oladi
        username=user.username,
        phone=user.phone,
        card=None 
    )
    db.add(new_user)
    db.commit()
    return {"status": "ok"}

@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)): 
    # Depends ichida yuqoridagi o'zimizning get_db funksiyasini chaqiramiz
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user

@app.get("/users-list/")
def get_users_list(search: str = None, db: Session = Depends(get_db)):
    query = db.query(models.User)
    if search:
        query = query.filter(models.User.full_name.contains(search))
    return query.all()

@app.post("/update-card/{user_id}")
def update_card(user_id: int, data: schemas.CardUpdateSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    
    user.card = data.card
    user.phone = data.phone
    db.commit()
    return {"status": "success"}

@app.post("/trees/")
def create_tree(tree: schemas.TreeCreate, db: Session = Depends(get_db)):
    new_tree = models.Tree(
        user_id=tree.user_id,
        user_name=tree.user_name,
        tree_type=tree.tree_type,
        latitude=tree.latitude,
        longitude=tree.longitude,
        photo=tree.photo,
        status="pending"
    )
    db.add(new_tree)
    db.commit()
    db.refresh(new_tree) # Yaratilgan ob'ektni ma'lumotlari bilan birga qaytarish uchun
    return {"message": "Success", "id": new_tree.id}

@app.get("/trees/")
def get_trees(db: Session = Depends(get_db)):
    return db.query(models.Tree).all()

@app.get("/photo/{file_id}")
def get_photo(file_id: str):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        r = requests.get(url).json()
        file_path = r["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        img = requests.get(file_url)
        return Response(content=img.content, media_type="image/jpeg")
    except Exception as e:
        # Xatolik yuz bersa dastur qotib qolmasligi uchun try/except ga olingan
        raise HTTPException(status_code=404, detail="Rasm topilmadi")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>GreenPay Admin Panel</title>
        <style>
            body { font-family: sans-serif; background: #f4f7f6; padding: 20px; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .nav button { padding: 10px 20px; margin-right: 5px; cursor: pointer; background: #ddd; border: none; border-radius: 5px; transition: 0.3s; }
            .nav button:hover { background: #ccc; }
            .nav button.active { background: #2ecc71; color: white; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background: #2ecc71; color: white; }
            img { width: 60px; border-radius: 5px; object-fit: cover; }
            a { color: #3498db; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌳 GreenPay Boshqaruv Paneli</h1>
            <div class="nav">
                <button id="btnTrees" class="active" onclick="switchTab('trees')">🌲 Daraxtlar</button>
                <button id="btnUsers" onclick="switchTab('users')">👤 Foydalanuvchilar</button>
            </div>
            <table>
                <thead><tr id="tableHead"></tr></thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>
        <script>
            let currentTab = 'trees';
            async function loadData() {
                try {
                    const res = await fetch(currentTab === 'trees' ? '/trees/' : '/users-list/');
                    const data = await res.json();
                    const head = document.getElementById('tableHead');
                    const body = document.getElementById('tableBody');
                    body.innerHTML = '';
                    
                    if (currentTab === 'trees') {
                        head.innerHTML = '<th>Foydalanuvchi</th><th>Daraxt</th><th>Rasm</th><th>Xarita</th>';
                        data.forEach(t => {
                            // Google Maps ssilkasi to'g'ri formatga keltirildi
                            let mapsLink = `https://www.google.com/maps?q=${t.latitude},${t.longitude}`;
                            body.innerHTML += `<tr>
                                <td><b>${t.user_name}</b><br><small>${t.phone || ''}</small></td>
                                <td>${t.tree_type}</td>
                                <td><img src="/photo/${t.photo}" alt="Daraxt rasmi"></td>
                                <td><a href="${mapsLink}" target="_blank">📍 Xaritada ko'rish</a></td>
                            </tr>`;
                        });
                    } else {
                        head.innerHTML = '<th>ID</th><th>Ism</th><th>Username</th><th>Telefon</th>';
                        data.forEach(u => {
                            body.innerHTML += `<tr>
                                <td>${u.user_id}</td>
                                <td><b>${u.full_name}</b></td>
                                <td>${u.username || '-'}</td>
                                <td>${u.phone || '-'}</td>
                            </tr>`;
                        });
                    }
                } catch (error) {
                    console.error("Ma'lumotlarni yuklashda xatolik yuz berdi:", error);
                }
            }
            
            function switchTab(tab) {
                currentTab = tab;
                document.getElementById('btnTrees').classList.toggle('active', tab === 'trees');
                document.getElementById('btnUsers').classList.toggle('active', tab === 'users');
                loadData();
            }
            
            window.onload = loadData;
        </script>
    </body>
    </html>
    """
