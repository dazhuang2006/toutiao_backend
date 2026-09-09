import asyncio

import models.news_models  # 注册 News 模型，避免 NewsAISummary 的 relationship 解析失败
import models.ai_summary
from sqlalchemy import delete
from sqlalchemy import select

from config.cache_conf import delete_cache
from config.db_conf import AsyncSessionLocal, engine
import llm.summarizer as summarizer
from llm.summarizer import summarize
from models.ai_summary import NewsAISummary
from models.news_models import News

NEWS_ID = 1
REQUEST_COUNT = 100


async def get_news_content(news_id: int) -> str:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(News.content).where(News.id == news_id)
        )
        content = result.scalar_one_or_none()

    if not content:
        raise RuntimeError(f"news_id={news_id} 不存在，无法取得真实新闻正文")
    return content


async def clear_previous_summary(news_id: int) -> None:
    """清掉 Redis 缓存和 MySQL 摘要，保证实验从冷启动开始。"""
    cache_key = summarizer._cache_key(news_id)
    await delete_cache(cache_key)

    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(NewsAISummary).where(NewsAISummary.news_id == news_id)
        )
        await session.commit()

    print(f"已清理: Redis {cache_key} / MySQL news_id={news_id}")


async def main():
    try:
        await clear_previous_summary(NEWS_ID)
        content = await get_news_content(NEWS_ID)
        print(f"已读取真实新闻正文: {len(content)} 字")

        summarizer.LLM_CALL_COUNT = 0

        for i in range(1, REQUEST_COUNT + 1):
            result = await summarize(news_id=NEWS_ID, content=content)
            print(i, result[:20])

        llm_calls = summarizer.LLM_CALL_COUNT
        reduced_calls = REQUEST_COUNT - llm_calls
        reduction_rate = reduced_calls / REQUEST_COUNT * 100

        print("\n指标\t结果")
        print(f"测试请求数\t{REQUEST_COUNT}")
        print(f"LLM 调用次数\t{llm_calls}")
        print(f"LLM 调用减少次数\t{reduced_calls}")
        print(f"LLM 调用减少率\t{reduced_calls}/{REQUEST_COUNT} = {reduction_rate:.0f}%")
    finally:
        await engine.dispose()


asyncio.run(main())
