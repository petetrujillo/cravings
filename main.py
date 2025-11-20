from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def init_db():
    conn = sqlite3.connect("cravings.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS cravings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        week TEXT,
        text TEXT
    )""")
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/crave")
async def crave(cravings: str = Form(...)):
    today = datetime.now().strftime("%Y-%m-%d")
    week = datetime.now().isocalendar()
    week_str = f"{week[0]}-W{week[1]:02d}"
    
    conn = sqlite3.connect("cravings.db")
    conn.execute("INSERT INTO cravings (date, week, text) VALUES (?, ?, ?)",
                 (today, week_str, cravings))
    conn.commit()
    conn.close()
    
    return {"status": "got it babe ❤️"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
