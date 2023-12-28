from abc import ABC, abstractmethod


class CacheConnection(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
