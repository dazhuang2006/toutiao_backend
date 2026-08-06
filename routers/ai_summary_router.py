from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from llm.summarizer import summarize
from models.news_models import News

router = APIRouter(prefix="/api/news", tags=["ai-summary"])


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