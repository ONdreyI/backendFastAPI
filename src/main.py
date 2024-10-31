from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.app.hotels import router as hotel_router
from src.app.auth import router as auth_router
from src.app.rooms import router as room_router
from src.app.bookings import router as bookings_router
from src.app.facilities import router as facilities_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


print(f"settings.DB_NAME={settings.DB_NAME}")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def func():
    return {"message": "Wellcome to the HOTELS!"}


app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(bookings_router)
app.include_router(facilities_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
