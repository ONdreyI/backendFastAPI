import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        """
        Get value by key.
        :param key:
        :return:
        """
        return await self.redis.get(key)

    async def delete(self, key: str):
        """
        Delete key from Redis.
        :param key:
        :return:
        """
        await self.redis.delete(key)

    async def close(self):
        """
        Close Redis connection.
        :return:
        """
        await self.redis.close()
