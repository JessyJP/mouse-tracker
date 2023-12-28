from abc import ABC, abstractmethod


class AbstractCache(ABC):

    @abstractmethod
    async def set(self, key: str, value: str):
        pass

    @abstractmethod
    async def get(self, key: str):
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass
