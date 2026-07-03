from redis.asyncio import Redis


class AIRedis:

    def __init__(self, redis: Redis):
        self.redis = redis

    def _summary_key(self, news_id: int) -> str:
        return f"news:summary:{news_id}"

    async def get_summary(self, news_id: int) -> str | None:
        return await self.redis.get(self._summary_key(news_id))

    async def set_summary(
        self,
        news_id: int,
        summary: str,
        expire: int = 60 * 60 * 24,
    ):
        await self.redis.set(
            self._summary_key(news_id),
            summary,
            ex=expire,
        )

    async def delete_summary(self, news_id: int):
        await self.redis.delete(self._summary_key(news_id))