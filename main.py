from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers.expenses import expenses_router
from api.routers.users import users_router
from db.init_db import init_db

app = FastAPI()

app.include_router(users_router)
app.include_router(expenses_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    yield
    # shutdown (опціонально)

app = FastAPI(lifespan=lifespan)
