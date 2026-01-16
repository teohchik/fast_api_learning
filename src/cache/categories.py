from src.cache.base import BaseCacheKeyBuilder


class CategoryCacheKeyBuilder(BaseCacheKeyBuilder):
    prefix = "categories"
    expire = 300
