from typing import Annotated, TypeAlias

from fastapi import Depends, Query, Header, HTTPException, status
from pydantic import BaseModel

from src.config.settings import settings


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(20, ge=1, le=100)]


PaginationDep: TypeAlias = Annotated[PaginationParams, Depends()]

API_KEY = settings.API_KEY


async def verify_bot_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
