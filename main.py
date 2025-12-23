from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

# Initialize FastAPI
app = FastAPI()

# ===== CORS configuration =====
# Allow only your GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rahul636390.github.io"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],   # allows POST, OPTIONS, GET
    allow_headers=["*"],
)

# ===== Pydantic model for contact form =====
class Contact(BaseModel):
    name: str
    email: str
    message: str

# ===== Contact endpoint =====
@app.post("/contact")
def contact(data: Contact):
    try:
        # Connect to SQLite database (creates file if not exists)
        conn = sqlite3.connect("contact.db")
        cursor = conn.cursor()

        # Create table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                message TEXT
            )
        """)

        # Insert submitted contact data
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (data.name, data.email, data.message)
        )

        conn.commit()
        conn.close()

        # Return success response
        return {"success": True, "message": "Message received successfully!"}

    except Exception as e:
        # Handle errors gracefully
        return {"success": False, "error": str(e)}



