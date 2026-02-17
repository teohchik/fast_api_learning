from fastapi import Request

from src.cache.base import BaseCacheKeyBuilder


class ExpensesCacheKeyBuilder(BaseCacheKeyBuilder):
    prefix = "expenses"
    expire = 1500

    @classmethod
    def build(cls, *args, request: Request = None, **kwargs) -> str:
        if request is None:
            return f"{cls.prefix}:unknown"

        user_id = cls._get_user_id(request)
        if user_id is None:
            return f"{cls.prefix}:no-user"

        year = request.query_params.get("year")
        month = request.query_params.get("month")
        page = request.query_params.get("page")
        per_page = request.query_params.get("per_page")

        key_parts = [f"{cls.prefix}:user:{user_id}"]

        if year and month:
            key_parts.append(f"year:{year}:month:{month}")

        if page and per_page:
            key_parts.append(f"page:{page}:per:{per_page}")

        return ":".join(key_parts)
