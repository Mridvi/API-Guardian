from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Response, HTTPException, status, Header, Depends
from contextlib import asynccontextmanager

from redis.asyncio import Redis
import os
from time import time
import math


BUCKET_REPLENISH_RATE = 2
BUCKET_CAPACITY = 10
TOKENS_PER_REQUEST = 1


async def get_script_hash(redis_client: Redis, rel_path_to_script: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(main_dir, rel_path_to_script)

    with open(script_path, "r") as f:
        script_content = f.read()

    return await redis_client.script_load(script_content)


redis_client = None
script_hash = None

request_stats = {
    "total_requests": 0,
    "successful_requests": 0,
    "rate_limited_requests": 0,
}

recent_requests = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client, script_hash
    redis_client = Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT")
    )

    script_hash = await get_script_hash(
        redis_client,
        "./request_rate_limiter.lua"
    )

    yield

    await redis_client.close()


app = FastAPI(lifespan=lifespan)

app.mount("/dashboard", 
          StaticFiles(directory="dashboard", html=True), 
          name="dashboard")


API_KEYS = {
    "demo-key-123",
    "premium-key-123",
}


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return x_api_key


@app.middleware("http")
async def check_request(request: Request, call_next):
    client_ip = request.client.host
    prefix = "request_rate_limiter." + client_ip

    keys = [prefix + ".tokens", prefix + ".timestamp"]
    args = [
        BUCKET_REPLENISH_RATE,
        BUCKET_CAPACITY,
        time(),
        TOKENS_PER_REQUEST
    ]

    allowed, new_tokens = await redis_client.evalsha(
        script_hash, len(keys), *keys, *args
    )

    retry_after = math.ceil(
        TOKENS_PER_REQUEST / BUCKET_REPLENISH_RATE
    )

    if allowed:
        request_stats["total_requests"] += 1

        response = await call_next(request)

        if response.status_code < 400:
            request_stats["successful_requests"] += 1

        recent_requests.append({
            "method": request.method,
            "endpoint": request.url.path,
            "status": response.status_code,
            "time": time()
        })

        if len(recent_requests) > 20:
            recent_requests.pop(0)

        response.headers["X-RateLimit-Remaining"] = str(new_tokens)
        response.headers["Retry-After"] = str(retry_after)
        response.headers["X-RateLimit-Limit"] = str(BUCKET_CAPACITY)

        return response

    else:


        request_stats["total_requests"] += 1
        request_stats["rate_limited_requests"] += 1

        recent_requests.append({
            "method": request.method,
            "endpoint": request.url.path,
            "status": 429,
            "time": time()
        })

        if len(recent_requests) > 20:
            recent_requests.pop(0)

        
        
        return Response(
            content="Too many requests",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            media_type="text/plain",
            headers={
                "X-RateLimit-Limit": str(BUCKET_CAPACITY),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(retry_after)
            },
        )


@app.get("/api/example")
def get_example(x_api_key: str = Depends(verify_api_key)):
    return {"message": "This is a rate limited endpoint"}

@app.get("/api/stats")
def get_stats():
    return request_stats

@app.get("/api/recent-requests")
def get_recent_requests():
    return recent_requests