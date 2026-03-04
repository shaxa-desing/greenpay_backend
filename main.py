from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/trees/")
def create_tree(tree: schemas.Tree, db: Session = Depends(get_db)):

    return crud.create_tree(db, tree)


@app.get("/trees/")
def get_trees(db: Session = Depends(get_db)):

    return crud.get_trees(db)


@app.get("/", response_class=HTMLResponse)
def dashboard():

    return """
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
            <div style="border:1px solid #ccc;padding:10px;margin:10px">

            <b>User:</b> ${tree.user_name}<br>
            <b>Telefon:</b> ${tree.phone}<br>
            <b>Daraxt:</b> ${tree.tree_type}<br>

            <img src="https://api.telegram.org/file/botTOKEN/${tree.photo}" width="200"/><br>

            <a href="https://maps.google.com/?q=${tree.latitude},${tree.longitude}" target="_blank">
            📍 Xarita
            </a>

            </div>
            `
        })

        document.getElementById("trees").innerHTML = html
    }

    </script>
    """
