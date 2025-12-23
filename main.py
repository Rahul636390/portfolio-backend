from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Allow frontend access (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[" https://rahul636390.github.io/portfolio-frontend/"],# later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contact(BaseModel):
    name: str
    email: str
    message: str

@app.post("/contact")
def contact(data: Contact):
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        (data.name, data.email, data.message)
    )

    conn.commit()
    conn.close()

    return {"success": True}


