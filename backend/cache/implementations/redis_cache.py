import redis
from backend.cache.abstractions.abstract_cache import AbstractCache


class RedisCache(AbstractCache):
    def __init__(self, cache_conn: redis.Redis):
        self._cache_conn = cache_conn

    async def set(self, key, value):
        pass

    async def get(self, key):
        await self._cache_conn.get(key)

    async def delete(self, key):
        await self._cache_conn.delete(key)

    async def queue_push(self, key, value):
        await self._cache_conn.rpush(key, value)

    async def queue_pop(self, key):
        return await self._cache_conn.lpop(key)

    async def get_queue_items(self, key, start, stop):
        return await self._cache_conn.lrange(key, start, stop)

    async def get_len(self, key):
        return await self._cache_conn.llen(key)
