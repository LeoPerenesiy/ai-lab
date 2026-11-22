from app.core.redis_client import redis_client


class RedisService:

    def set(self, key: str, value: str, expire: int | None = None) -> None:
        redis_client.set(key, value, ex=expire)

    def get(self, key: str) -> str | None:
        return redis_client.get(key)

    def delete(self, key: str) -> None:
        redis_client.delete(key)

    def exists(self, key: str) -> bool:
        return bool(redis_client.exists(key))

    def ping(self) -> bool:
        return bool(redis_client.ping())
