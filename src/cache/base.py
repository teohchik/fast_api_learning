from fastapi import Request


class BaseCacheKeyBuilder:
    prefix = None

    @classmethod
    def build(cls, *args, request: Request = None, **kwargs) -> str:
        if request is None:
            return f"{cls.prefix}:unknown"

        user_id = cls._get_user_id(request)
        if user_id is None:
            return f"{cls.prefix}:no-user"

        page = request.query_params.get("page")
        per_page = request.query_params.get("per_page")

        if page and per_page:
            return f"{cls.prefix}:user:{user_id}:page:{page}:per:{per_page}"

        return f"{cls.prefix}:user:{user_id}"

    @staticmethod
    def _get_user_id(request: Request):
        path_params = request.scope.get("path_params", {})
        return path_params.get("user_id") or request.query_params.get("user_id")

    @classmethod
    def generate_pattern(cls, user_id) -> str:
        return f"{cls.prefix}:user:{user_id}*"
