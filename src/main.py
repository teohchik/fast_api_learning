import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.routers.categories import category_router
from src.api.routers.expenses import expenses_router
from src.api.routers.users import users_router
from src.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(expenses_router)
app.include_router(category_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
