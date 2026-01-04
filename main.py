from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers.expenses import expenses_router
from api.routers.users import users_router
from db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(expenses_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
