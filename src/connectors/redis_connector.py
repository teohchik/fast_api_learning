import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def set_value(self, key: str, value: str, expire: int = None):
        await self.redis.set(key, value, ex=expire)

    async def get_value(self, key: str):
        return await self.redis.get(key)

    async def delete_value(self, key: str):
        await self.redis.delete(key)


    async def scan_delete(self, pattern: str):
        async for key in self.redis.scan_iter(match=pattern):
            print(f"Deleting key: {key.decode('utf-8')}")
            await self.redis.delete(key)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
