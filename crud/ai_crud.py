from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.ai_summary import NewsAISummary

#新闻id查摘要
async def get_by_news_id(news_id: int, db: AsyncSession = Depends(get_db))->NewsAISummary|None:
    stmt=select(NewsAISummary).where(NewsAISummary.news_id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()

#创建摘要
async def create_summary(news_id: int, summary: str,model_name: str,
                         prompt_version: str="v1", db: AsyncSession = Depends(get_db))->NewsAISummary:
    ai_summary=NewsAISummary(news_id=news_id,summary=summary,
                             model_name=model_name,prompt_version=prompt_version,status=1)
    db.add(ai_summary)
    await db.commit()
    await db.refresh(ai_summary)
    return ai_summary

#更新摘要
async def update_summary(news_id: int, summary: str,model_name: str,
                         prompt_version: str="v1", db: AsyncSession = Depends(get_db))->NewsAISummary:
    stmt=(update(NewsAISummary).where(NewsAISummary.news_id==news_id)
          .values(summary=summary,model_name=model_name,status=1))
    await db.execute(stmt)
    await db.commit()
    return await get_by_news_id(news_id, db)

#删除摘要
async def delete_summary(news_id: int, db: AsyncSession = Depends(get_db)):
    stmt=delete(NewsAISummary).where(NewsAISummary.news_id==news_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0