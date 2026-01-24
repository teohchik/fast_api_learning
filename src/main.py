import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend

from src.config.settings import settings

sys.path.append(str(Path(__file__).parent.parent))

from src.api.routers.categories import category_router
from src.api.routers.expenses import expenses_router
from src.api.routers.users import users_router
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await init_db()
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.disconnect()


if settings.MODE == "TEST":
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(expenses_router)
app.include_router(category_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
