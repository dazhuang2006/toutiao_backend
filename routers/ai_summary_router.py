import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from llm.agent import news_agent
from llm.rag import qa_chain, search_news
from llm.summarizer import summarize
from models.news_models import News
from schemas.ask_sch import AskRequest

router = APIRouter(prefix="/api/news", tags=["ai-summary"])


@router.post("/ask")
async def ask_news(data: AskRequest):
    sources = await asyncio.to_thread(search_news, data.question)
    answer = await qa_chain.ainvoke({"question": data.question})
    return {
        "code": 200,
        "message": "success",
        "data": {
            "answer": answer,
            "sources": [
                {
                    "newsId": s["news_id"],
                    "title": s["title"],
                    "score": round(s["score"], 4),
                }
                for s in sources
            ],
        },
    }


@router.post("/agent")
async def ask_news_agent(data: AskRequest):
    result = await news_agent.ainvoke(
        {"messages": [{"role": "user", "content": data.question}]}
    )
    return {
        "code": 200,
        "message": "success",
        "data": {"answer": result["messages"][-1].content},
    }


@router.get("/ai-summary")
async def get_ai_summary(
    news_id: int = Query(..., alias="id"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar_one_or_none()

    if news is None:
        raise HTTPException(status_code=404, detail="新闻不存在")

    summary = await summarize(news_id=news.id, content=news.content)

    return {
        "code": 200,
        "message": "success",
        "data": {"summary": summary},
    }
