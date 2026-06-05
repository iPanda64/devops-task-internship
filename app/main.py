"""Simple FastAPI app with a Redis-backed visit counter."""

import os

import redis
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = FastAPI(title="DevOps Intern Demo", version="0.1.0")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


### Bakend API endpoints
@app.get("/health")
def health(response: Response) -> dict:
    try:
        r.ping()
        redis_ok = True
        status_text = "ok"
    except redis.RedisError:
        status_text = "unhealthy"
        redis_ok = False
        response.status_code = 503
    return {"status": status_text, "redis": redis_ok}

@app.get("/visits")
def visits() -> dict:
    count = r.incr("visits")
    return {"visits": count}

@app.get("/visits/count")
def get_visits_count() -> dict:
    count = r.get("visits")
    return {"visits": int(count) if count else 0}

@app.post("/visits/reset")
def reset_visits() -> dict:
    r.set("visits", 0)
    return {"visits": 0}



# Minimal UI
@app.get("/index", response_class=HTMLResponse)
def index() -> str:
    visits_count = r.get("visits") or 0
    return f"""
    <html>
        <head><title>Counter</title></head>
        <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>Visits: {visits_count}</h1>
            <button onclick="fetch('/visits/reset', {{method: 'POST'}}).then(() => location.reload())">
                Reset Counter
            </button>
        </body>
    </html>
    """
