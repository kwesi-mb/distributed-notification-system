from redis import Redis
from redis.exceptions import ConnectionError

from app.core.config import settings


try:

    redis_client = Redis.from_url(
        settings.REDIS_URL,
        decode_response=True,
    )

    redis_client.ping()

except ConnectionError as exc:
    raise RuntimeError(
        "Unable to connect to Redis."
    ) from exc 

