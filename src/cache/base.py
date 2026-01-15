from fastapi import Request
from fastapi_cache import FastAPICache


class BaseCacheKeyBuilder:
    prefix = None

    @classmethod
    def build(cls, *args, request: Request = None, **kwargs) -> str:
        if request is None:
            return f"{cls.prefix}/unknown"

        params = request.query_params

        user_id = params.get("user_id")
        if user_id is None:
            return f"{cls.prefix}:no-user"

        page = params.get("page")
        per_page = params.get("per_page")
        if page is None or per_page is None:
            return f"{cls.prefix}/user_id:{user_id}"

        return f"{cls.prefix}/user_id:{user_id}/page:{page}/per_page:{per_page}"

    @classmethod
    async def invalidate_by_pattern(cls, user_id):
        redis = FastAPICache.get_backend().redis
        async for key in redis.scan_iter(match=f"{cls.prefix}/user_id:{user_id}*"):
            print("Deleting cache key:", key)
            await redis.delete(key)
