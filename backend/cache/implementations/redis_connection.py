from backend.cache.abstractions.cache_connection import CacheConnection
import redis.asyncio as redis


class RedisConnection(CacheConnection):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._connection = None

    def connect(self):
        self._connection = redis.Redis(*self._args, **self._kwargs)
        return self._connection

    async def close(self):
        if self._connection:
            await self._connection.close()
