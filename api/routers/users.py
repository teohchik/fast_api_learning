from fastapi import APIRouter

from schemas.models import User

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post("/", response_model=User)
def create_user(new_user: User):
    return new_user
