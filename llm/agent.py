from langchain.agents import create_agent
from langchain_core.tools import tool
from sqlalchemy import select

from config.db_conf import AsyncSessionLocal
from llm.model import model
from llm.rag import format_docs, search_news
from llm.summarizer import summarize
from models.news_models import News


@tool
def search_news_tool(query: str) -> str:
    """根据用户问题在新闻知识库中检索最相关的新闻片段，返回片段和对应标题。"""
    return format_docs(search_news(query))


@tool
async def get_news_summary_tool(news_id: int) -> str:
    """根据新闻 ID 获取该新闻的 AI 摘要。"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(News).where(News.id == news_id))
        news = result.scalar_one_or_none()

    if news is None:
        return f"新闻 {news_id} 不存在"

    return await summarize(news_id=news.id, content=news.content)


AGENT_SYSTEM_PROMPT = (
    "你是一名新闻助手。回答用户问题前，优先使用工具检索新闻知识库；"
    "回答要基于工具返回的资料，并给出相关新闻标题；资料中没有的信息要明确说不知道。"
)

news_agent = create_agent(
    model=model,
    tools=[search_news_tool, get_news_summary_tool],
    system_prompt=AGENT_SYSTEM_PROMPT,
)
