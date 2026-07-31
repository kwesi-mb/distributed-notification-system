import json
from typing import Any

from redis.exceptions import RedisError

from app.core.redis import redis_client 

class CacheService:

    def get(self, key: str) -> Any | None:
        """
        Retrieve a value from Redis.
        """

        try:
            value = redis_client.get(key)

            if value is None:
                return None

            return json.loads(value)

        except RedisError:
            return None 

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 1800,
    ) -> bool:
        """
        Store a JSON value in Redis.
        """

        try:
            redis_client.set(
                key,
                json.dumps(value),
                ex=ttl,
            )

            return True

        except RedisError:
            return False

    def delete(
        self,
        key: str,
    )-> bool:
        """
        Delete a cache entry.
        """

        try: 
            redis_client.delete(key)

            return True

        except RedisError:
            return False 

    def exists(
        self,
        key: str,
    ) -> bool:

        try:
            return bool(
                redis_client.exists(key)
            )

        except RedisError:
            return False 

    def ttl(
        self,
        key: str,
    ) -> int:

        try: 
            return redis_client.ttl(key)

        except RedisError:
            return -1
