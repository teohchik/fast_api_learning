from typing import Annotated, TypeAlias

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(20, ge=1, le=100)]

PaginationDep: TypeAlias = Annotated[PaginationParams, Depends()]

