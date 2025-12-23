from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import random
import string
import json
import redis.asyncio as redis
import os
from datetime import datetime

from .database import get_db
from .models import URL

app = FastAPI(title="URL Shortener API")

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(redis_url, decode_responses=True)

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
async def redirect_url(short_code: str, db: AsyncSession = Depends(get_db)):
    # 1. CHECK CACHE (Fast path)
    cached_url = await r.get(f"url:{short_code}")
    if cached_url:
        # Fire-and-forget analytics event (push to queue)
        await r.lpush("analytics_queue", short_code)
        return RedirectResponse(url=cached_url)

    # 2. DATABASE FALLBACK (Slow Path)
    result = await db.execute(select(URL).filter(URL.short_code == short_code))
    url_entry = result.scalars().first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # 3. POPULATE CACHE (Set TTL to 1 hour)
    await r.set(f"url:{short_code}", url_entry.original_url, ex=3600)

    # Push analytics event
    await r.lpush("analytics_queue", short_code)
    
    return RedirectResponse(url=url_entry.original_url)