from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import random
import string

from .database import get_db
from .models import URL

app = FastAPI(title="URL Shortener API")

class URLCreate(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "api"}

@app.post("/api/shorten")
async def shorten_url(item: URLCreate, db: AsyncSession = Depends(get_db)):
    # Generate code
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Save to Postgres
    new_url = URL(short_code=short_code, original_url=item.url)
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)

    return {"short_code": new_url.short_code, "original_url": new_url.original_url}

@app.get("/{short_code}")
async def redirect_url(short_code: int, db: AsyncSession = Depends(get_db)):
    # Query Postgres
    result = await db.execute(select(URL).filter(URL.short_code == short_code))
    url_entry = result.scalars().first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {"action": "redirect", "url":url_entry.original_url}