from backend.cache.implementations.redis_cache import RedisCache
from backend.sql.connection import Database
from backend.utils.batch_manager import BatchManager
from backend.utils.singleton_manager import SingletonManager
from backend.cache.implementations.redis_connection import RedisConnection
from backend.websockets.websocket_manager import WebSocketManager


class SetUp:
    def __init__(self):
        self.websocket_manager = None
        self.redis = None
        self.batch_manager = None
        self.initialize_services()

    def initialize_services(self):
        redis_connection = SingletonManager.get_instance(RedisConnection, host='localhost', port=6379, db=0)
        connected_redis = redis_connection.connect()

        self.redis = RedisCache(connected_redis)
        self.batch_manager = BatchManager(self.redis)
        self.websocket_manager = SingletonManager.get_instance(WebSocketManager)

    @staticmethod
    async def close_services():
        """Utilizes SingletonManager to close all managed instances"""

        if Database.pool is not None:
            Database.pool.close()
            await Database.pool.wait_closed()

        await SingletonManager.close_all()
