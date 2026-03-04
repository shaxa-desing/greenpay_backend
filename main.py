from fastapi.responses import HTMLResponse


@app.get("/", response_class=HTMLResponse)
def dashboard():

    html = """
    <html>
    <head>
        <title>GreenPay Dashboard</title>
    </head>

    <body style="font-family:Arial">

        <h1>🌳 GreenPay Dashboard</h1>

        <button onclick="loadTrees()">Daraxtlarni yuklash</button>

        <div id="trees"></div>

        <script>

        async function loadTrees(){

            const res = await fetch("/trees/")
            const data = await res.json()

            let html = ""

            data.forEach(tree => {

                html += `
                <div style="border:1px solid #ccc;padding:10px;margin:10px">

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

    </body>
    </html>
    """

    return html
