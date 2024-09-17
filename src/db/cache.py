from db.base_cache import AsyncCache


async_cache: AsyncCache | None = None


async def get_async_cache() -> AsyncCache:
    return async_cache
