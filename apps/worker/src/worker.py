import os
import redis
import time
from sqlalchemy import create_engine, text

# Worker uses sync drivers (simpler for background jobs)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/url_shortener")

# Connect to Redis
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Connect to DB
engine = create_engine(DATABASE_URL)

print("Worker started. Waiting for events...")

while True:
    # Blocking pop: waits until an item is available in the queue
    # returns tuple('queue_name', value)
    task = r.blpop("analytics_queue", timeout=0)

    if task:
        short_code = task[1]
        print(f"Processing click for: {short_code}")
        
        try:
            with engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO analytics (short_code) VALUES (:code)"),
                    {"code": short_code}
                )
                conn.commit()
        except Exception as e:
            print(f"Error saving analytics: {e}")