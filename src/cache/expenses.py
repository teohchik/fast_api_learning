from src.cache.base import BaseCacheKeyBuilder


class ExpensesCacheKeyBuilder(BaseCacheKeyBuilder):
    prefix = "expenses"
