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
    """Yangi foydalanuvchini ro'yxatdan o'tkazish"""
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user:
        return db_user
    new_user = models.User(user_id=user.user_id, full_name=user.user_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GreenPay Dashboard</title>
        <style>
            :root { --primary: #2ecc71; --dark: #2c3e50; --bg: #f8f9fa; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); margin: 0; padding: 20px; color: var(--dark); }
            .container { max-width: 1200px; margin: 0 auto; }
            header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 2px solid var(--primary); padding-bottom: 10px; }
            h1 { color: var(--primary); margin: 0; font-size: 28px; }
            .btn-refresh { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; transition: 0.3s; }
            .btn-refresh:hover { background: #27ae60; transform: scale(1.05); }
            #trees-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
            .card { background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: 0.3s; position: relative; }
            .card:hover { transform: translateY(-5px); }
            .card img { width: 100%; height: 200px; object-fit: cover; background: #eee; }
            .card-body { padding: 15px; }
            .user-name { font-weight: bold; font-size: 18px; margin-bottom: 5px; color: var(--dark); }
            .tree-type { color: var(--primary); font-weight: 600; margin-bottom: 10px; }
            .info { font-size: 14px; color: #666; margin-bottom: 15px; }
            .btn-map { display: block; text-align: center; background: #3498db; color: white; text-decoration: none; padding: 8px; border-radius: 5px; font-size: 14px; transition: 0.3s; }
            .btn-map:hover { background: #2980b9; }
            .loading { text-align: center; font-size: 18px; color: #999; margin-top: 50px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🌳 GreenPay Dashboard</h1>
                <button class="btn-refresh" onclick="loadTrees()">🔄 Yangilash</button>
            </header>
            <div id="trees-grid"><p class="loading">Daraxtlar yuklanmoqda...</p></div>
        </div>

        <script>
            async function loadTrees() {
                const grid = document.getElementById("trees-grid");
                try {
                    const res = await fetch('/trees/');
                    const data = await res.json();
                    
                    if (data.length === 0) {
                        grid.innerHTML = '<p class="loading">Hozircha daraxtlar yo'q.</p>';
                        return;
                    }

                    grid.innerHTML = data.map(t => `
                        <div class="card">
                            <img src="/photo/${t.photo}" alt="Daraxt rasmi">
                            <div class="card-body">
                                <div class="user-name">${t.user_name}</div>
                                <div class="tree-type">🌲 ${t.tree_type}</div>
                                <div class="info">📍 Koordinata: ${t.latitude.toFixed(4)}, ${t.longitude.toFixed(4)}</div>
                                <a href="https://www.google.com/maps?q=${t.latitude},${t.longitude}" target="_blank" class="btn-map">🗺️ Xaritada ko'rish</a>
                            </div>
                        </div>
                    `).join('');
                } catch (err) {
                    grid.innerHTML = '<p class="loading" style="color:red;">Xatolik yuz berdi!</p>';
                }
            }
            // Sahifa yuklanganda ma'lumotlarni olish
            window.onload = loadTrees;
        </script>
    </body>
    </html>
    """
