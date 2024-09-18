from abc import ABC, abstractmethod


class AsyncCache(ABC):
    @abstractmethod
    async def get(self, **params):
        raise NotImplementedError

    @abstractmethod
    async def put(self, **params):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError

    @abstractmethod
    async def exists(self, **params):
        raise NotImplementedError
