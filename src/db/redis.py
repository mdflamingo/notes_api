from typing import Any
import json

from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from db.base_cache import AsyncCache
from core.config import settings


class RedisAsyncCache(AsyncCache):

    def __init__(self) -> None:
        self._redis = Redis(host=settings.redis_host, port=settings.redis_port)

    async def get(self, key: str) -> Any | None:
        if data := await self._redis.get(key):
            return data

        return None

    async def put(self, key, ttl, value=True):
        json_response = jsonable_encoder(value)
        value_str = json.dumps(json_response)
        await self._redis.setex(key, ttl, value=value_str)

    async def exists(self, key):
        return await self._redis.exists(key)

    async def close(self) -> None:
        await self._redis.close()
