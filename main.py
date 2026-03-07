from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy import Column, Integer, String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import Session
import database, models, schemas, crud, requests
from typing import Optional

app = FastAPI(title="GreenPay API")

# Ma'lumotlar bazasini yaratish
models.Base.metadata.create_all(bind=database.engine)

BOT_TOKEN = "8565818987:AAEciIAbwHVGjkuJ7TwwdCfKjKlXYj8annI"

# ----------------------------------------------------------------
# API ENDPOINTS
# ----------------------------------------------------------------

@app.get("/users-list/")
def get_users_list(search: str = None, db: Session = Depends(database.get_db)):
    query = db.query(models.User)
    if search:
        query = query.filter(models.User.full_name.contains(search))
    return query.all()

@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    print(f"Qidirilayotgan ID: {user_id}") # Loglarda ID ko'rinishi kerak
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    
    if not user:
        print("Foydalanuvchi bazada topilmadi!") # Buni loglarda tekshiring
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
        
    return user

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    print(f"DEBUG: Kelgan ma'lumot -> ID: {user.user_id}, Name: {user.user_name}") # <--- SHUNI QO'SHING
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user:
        return db_user
    new_user = models.User(user_id=user.user_id, full_name=user.user_name, username=user.username, phone=user.phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/trees/")
def get_trees(db: Session = Depends(database.get_db)):
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
    except:
        raise HTTPException(status_code=404)

# ----------------------------------------------------------------
# DASHBOARD (HTML)
# ----------------------------------------------------------------

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
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background: #2ecc71; color: white; }
            .btn-map { color: #3498db; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌳 GreenPay Boshqaruv Paneli</h1>
            <button onclick="switchTab('trees')">🌲 Daraxtlar</button>
            <button onclick="switchTab('users')">👤 Foydalanuvchilar</button>

            <table id="dataTable">
                <thead><tr id="tableHead"></tr></thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>

        <script>
            let currentTab = 'trees';

            async function loadData() {
                const res = await fetch(currentTab === 'trees' ? '/trees/' : '/users-list/');
                const data = await res.json();
                const head = document.getElementById('tableHead');
                const body = document.getElementById('tableBody');
                body.innerHTML = '';

                if (currentTab === 'trees') {
                    head.innerHTML = '<th>Foydalanuvchi</th><th>Daraxt</th><th>Xarita</th>';
                    data.forEach(t => {
                        body.innerHTML += `
                            <tr>
                                <td><b>${t.user_name || 'Noma\'lum'}</b><br><small>${t.phone || ''}</small></td>
                                <td>${t.tree_type}</td>
                                <td>
                                    <a href="https://www.google.com/maps?q=${t.latitude},${t.longitude}" target="_blank" class="btn-map">
                                        📍 Xaritada ko'rish
                                    </a>
                                </td>
                            </tr>`;
                    });
                } else {
                    head.innerHTML = '<th>ID</th><th>FMI</th><th>Username</th><th>Telefon</th>';
                    data.forEach(u => {
                        body.innerHTML += `
                            <tr>
                                <td>${u.user_id}</td>
                                <td>${u.full_name}</td>
                                <td>${u.username || '-'}</td>
                                <td>${u.phone || '-'}</td>
                            </tr>`;
                    });
                }
            }

            function switchTab(tab) { currentTab = tab; loadData(); }
            window.onload = loadData;
        </script>
    </body>
    </html>
    """
