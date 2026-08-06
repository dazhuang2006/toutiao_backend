from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from sqlalchemy import select

from config.cache_conf import get_cache, set_cache
from config.db_conf import AsyncSessionLocal
from llm.model import model
from models.ai_summary import NewsAISummary

PROMPT = """你是一名专业新闻编辑。
请阅读下面新闻，并生成一段摘要。
要求：
1. 保持客观
2. 不添加原文没有的信息
3. 控制在100字以内
4. 使用中文

新闻内容：
{content}
"""

summary_chain = PromptTemplate.from_template(PROMPT) | model | StrOutputParser()

CACHE_EXPIRE = 60 * 60 * 24  # 24小时


def _cache_key(news_id: int) -> str:
    return f"news:summary:{news_id}"


#按 Redis -> MySQL -> DeepSeek -> 写库 -> 回填缓存的顺序生成摘要
async def summarize(news_id: int, content: str) -> str:
    cache_key = _cache_key(news_id)

    cached = await get_cache(cache_key)
    if cached:
        return cached

    summary = await get_summary_from_db(news_id)
    if summary:
        await set_cache(cache_key, summary, expire=CACHE_EXPIRE)
        return summary

    summary = await summary_chain.ainvoke({"content": content})
    await save_summary(news_id, summary)
    await set_cache(cache_key, summary, expire=CACHE_EXPIRE)
    return summary

#根据新闻 ID，从数据库查询已经预生成好的 AI 摘要；查到返回摘要字符串，查不到返回 None
async def get_summary_from_db(news_id: int) -> str | None:
    #开启一个异步会话
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(NewsAISummary).where(NewsAISummary.news_id == news_id)
        )
        row = result.scalar_one_or_none()
        return row.summary if row else None

#生成好的 AI 摘要写入数据库表 NewsAISummary
async def save_summary(news_id: int, summary: str) -> None:
    async with AsyncSessionLocal() as session:
        session.add(
            NewsAISummary(
                news_id=news_id,
                summary=summary,
                model_name="deepseek:deepseek-v4-flash",
                prompt_version="v1",
                status=1,
            )
        )
        await session.commit()
