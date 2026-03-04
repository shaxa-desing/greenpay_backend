from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

trees = []

class Tree(BaseModel):
    user_id: int
    user_name: str
    phone: str
    tree_type: str
    latitude: float
    longitude: float
    photo: str


@app.post("/trees/")
def create_tree(tree: Tree):
    trees.append(tree)
    return {"status": "saved"}


@app.get("/trees/")
def get_trees():
    return trees


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
            <div style="border:1px solid black;padding:10px;margin:10px">

            <b>User:</b> ${tree.user_name}<br>
            <b>Telefon:</b> ${tree.phone}<br>
            <b>Daraxt:</b> ${tree.tree_type}<br>

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
