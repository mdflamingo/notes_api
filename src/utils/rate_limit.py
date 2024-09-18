import datetime
from redis import Redis

from core.config import settings

redis_conn = Redis(host=settings.redis_host, port=settings.redis_port, db=0)


def rate_limit(user_id: str, request_limit_per_minute: int) -> bool:

    now = datetime.datetime.now()
    key = f'{user_id}:{now.minute}'
    pipe = redis_conn.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, 59)
    result = pipe.execute()
    request_number = result[0]

    if request_number > request_limit_per_minute:
        return False

    return True
