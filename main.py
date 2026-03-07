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
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user:
        return db_user
    new_user = models.User(
        user_id=user.user_id, 
        full_name=user.user_name,
        username=user.username,
        phone=user.phone
    )
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
            :root { --primary: #2ecc71; --dark: #2c3e50; --bg: #f8f9fa; }
            body { font-family: 'Segoe UI', sans-serif; background: var(--bg); margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
            .nav { margin-bottom: 20px; }
            .nav button { padding: 10px 20px; cursor: pointer; border: none; border-radius: 5px; margin-right: 10px; background: #ddd; }
            .nav button.active { background: var(--primary); color: white; }
            .search-box { margin-bottom: 20px; display: flex; gap: 10px; }
            input { padding: 10px; border: 1px solid #ccc; border-radius: 5px; flex: 1; }
            table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
            th { background: #f4f4f4; }
            img { width: 60px; border-radius: 5px; }
            .btn-map { color: #3498db; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header"><h1>🌳 GreenPay Dashboard</h1></div>
            
            <div class="nav">
                <button id="btnTrees" class="active" onclick="switchTab('trees')">🌲 Daraxtlar</button>
                <button id="btnUsers" onclick="switchTab('users')">👤 Foydalanuvchilar</button>
            </div>

            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Qidirish...">
                <button onclick="loadData()">🔍 Qidirish</button>
            </div>

            <div id="table-container">
                <table id="dataTable">
                    <thead><tr id="tableHead"></tr></thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
        </div>

        <script>
            let currentTab = 'trees';

            async function loadData() {
                const search = document.getElementById('searchInput').value;
                const url = currentTab === 'trees' ? '/trees/' : `/users-list/?search=${search}`;
                const res = await fetch(url);
                const data = await res.json();
                
                const head = document.getElementById('tableHead');
                const body = document.getElementById('tableBody');
                body.innerHTML = '';

                if (currentTab === 'trees') {
                    head.innerHTML = '<th>Foydalanuvchi</th><th>Daraxt turi</th><th>Rasm</th><th>Xarita</th>';
                    data.forEach(t => {
                        body.innerHTML += `
                            <tr>
                                <td><b>${t.user_name || 'Noma'lum'}</b><br><small>${t.phone || ''}</small></td>
                                <td>${t.tree_type}</td>
                                <td><img src="/photo/${t.photo}"></td>
                                <td>
                                    <a href="https://www.google.com/maps?q=${t.latitude},${t.longitude}" target="_blank" class="btn-map">
                                        📍 Xaritada ko'rish
                                    </a>
                                </td>
                            </tr>`;
                    });
                } else {
                    head.innerHTML = '<th>FMI</th><th>Username</th><th>Telefon</th><th>Karta</th>';
                    data.forEach(u => {
                        body.innerHTML += `
                            <tr>
                                <td><b>${u.full_name}</b></td>
                                <td>${u.username || '—'}</td>
                                <td>${u.phone || '—'}</td>
                                <td>${u.card || '—'}</td>
                            </tr>`;
                    });
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
