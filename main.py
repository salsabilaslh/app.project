from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("quotes.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {"message": "Quotes API is running"}

@app.get("/quotes")
def get_quotes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quotes")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]