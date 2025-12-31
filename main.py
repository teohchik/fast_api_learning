from fastapi import FastAPI

from api.routers.expenses import expenses_router
from api.routers.users import users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(expenses_router)
