from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import database, models, schemas, crud, requests

app = FastAPI(title="GreenPay API")

# Ma'lumotlar bazasi jadvallarini yaratish
models.Base.metadata.create_all(bind=database.engine)

BOT_TOKEN = "8565818987:AAEciIAbwHVGjkuJ7TwwdCfKjKlXYj8annI"

# ----------------------------------------------------------------
# API ENDPOINTS (Bot va Dashboard uchun)
# ----------------------------------------------------------------

@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    """Foydalanuvchi ma'lumotlarini olish (Shaxsiy kabinet uchun)"""
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user:
        return db_user
    
    # schemas.UserCreate dagi 'user_name' ni models.User dagi 'full_name' ga o'giramiz
    new_user = models.User(
        user_id=user.user_id, 
        full_name=user.user_name  # user.user_name deb yozilganiga e'tibor bering
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users-list/")
def get_users_list(search: str = None, db: Session = Depends(database.get_db)):
    query = db.query(models.User)
    if search:
        # Ism bo'yicha qidirish (full_name ustunidan)
        query = query.filter(models.User.full_name.contains(search))
    return query.all()

@app.post("/trees/")
def create_tree(tree: schemas.Tree, db: Session = Depends(database.get_db)):
    """Botdan kelgan yangi daraxt ma'lumotlarini saqlash"""
    return crud.create_tree(db, tree)

@app.get("/trees/")
def get_trees(db: Session = Depends(database.get_db)):
    """Barcha daraxtlarni dashboard uchun olish"""
    return crud.get_trees(db)

@app.post("/update_payment/")
def update_payment(data: schemas.PaymentUpdate, db: Session = Depends(database.get_db)):
    """Foydalanuvchi to'lov ma'lumotlarini yangilash"""
    user = db.query(models.User).filter(models.User.user_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    if data.card: user.card = data.card
    if data.phone_pay: user.phone_pay = data.phone_pay
    db.commit()
    return {"status": "success", "message": "Ma'lumotlar yangilandi"}

@app.get("/photo/{file_id}")
def get_photo(file_id: str):
    """Telegram file_id orqali rasmni dashboardda ko'rsatish"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        r = requests.get(url).json()
        file_path = r["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        img = requests.get(file_url)
        return Response(content=img.content, media_type="image/jpeg")
    except Exception:
        raise HTTPException(status_code=404, detail="Rasm yuklashda xatolik")

# ----------------------------------------------------------------
# DASHBOARD (Chiroyli interfeys)
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
            :root { --primary: #2ecc71; --secondary: #3498db; --bg: #f4f7f6; }
            body { font-family: sans-serif; background: var(--bg); margin: 0; padding: 20px; }
            .container { max-width: 1100px; margin: 0 auto; }
            .controls { display: flex; gap: 10px; margin-bottom: 20px; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; color: white; background: var(--primary); font-weight: bold; }
            .tabs { margin-bottom: 20px; }
            .tab-btn { background: #ddd; color: #333; margin-right: 5px; }
            .tab-btn.active { background: var(--secondary); color: white; }
            table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
            th { background: #f8f9fa; }
            .user-card { background: white; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 5px solid var(--primary); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌳 GreenPay Boshqaruv Paneli</h1>
            
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('trees')">🌲 Daraxtlar</button>
                <button class="tab-btn" onclick="switchTab('users')">👤 Foydalanuvchilar</button>
            </div>

            <div class="controls">
                <input type="text" id="searchInput" placeholder="Ism yoki ma'lumot qidirish...">
                <button onclick="performSearch()">🔍 Qidirish</button>
                <button style="background:#95a5a6" onclick="resetView()">🔄 Yangilash</button>
            </div>

            <div id="content">
                </div>
        </div>

        <script>
            let currentTab = 'trees';

            async function loadData(search = '') {
                const content = document.getElementById("content");
                const url = currentTab === 'trees' ? '/trees/' : `/users-list/?search=${search}`;
                
                try {
                    const res = await fetch(url);
                    const data = await res.json();
                    renderData(data);
                } catch (err) {
                    content.innerHTML = "<p style='color:red'>Ma'lumot yuklashda xato!</p>";
                }
            }

            function renderData(data) {
                const content = document.getElementById("content");
                if (data.length === 0) { content.innerHTML = "<p>Ma'lumot topilmadi.</p>"; return; }

                if (currentTab === 'trees') {
                    content.innerHTML = "<table><tr><th>Foydalanuvchi</th><th>Daraxt turi</th><th>Rasm</th></tr>" + 
                        data.map(t => `<tr><td>${t.user_name}</td><td>${t.tree_type}</td><td><a href="/photo/${t.photo}" target="_blank">Ko'rish</a></td></tr>`).join('') + "</table>";
                } else {
                    content.innerHTML = "<table><tr><th>ID</th><th>FMI</th><th>Karta</th><th>Telefon</th></tr>" + 
                        data.map(u => `<tr><td>${u.user_id}</td><td><b>${u.full_name}</b></td><td>${u.card || '—'}</td><td>${u.phone_pay || '—'}</td></tr>`).join('') + "</table>";
                }
            }

            function switchTab(tab) {
                currentTab = tab;
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                event.target.classList.add('active');
                loadData();
            }

            function performSearch() {
                const query = document.getElementById("searchInput").value;
                loadData(query);
            }

            function resetView() {
                document.getElementById("searchInput").value = '';
                loadData();
            }

            window.onload = loadData;
        </script>
    </body>
    </html>
    """
