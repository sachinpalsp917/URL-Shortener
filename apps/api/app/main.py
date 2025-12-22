from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string

app = FastAPI(title="URL Shortener API", version="1.0.0")

# Temporary in-memory DB for phase 1
fake_db = {}

class URLCreate(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "api"}

@app.post("/api/shorten")
def shorten_url(item: URLCreate):
    # Generate a random 6-character code
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    fake_db[short_code] = item.url
    return {"short_code": short_code, "original_url": item.url}

@app.get("/{short_code}")
def redirect_url(short_code: int):
    url = fake_db.get(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"action": "redirect", "url":url}