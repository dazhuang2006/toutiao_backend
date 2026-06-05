from models.news_models import Categroy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

#新闻分类列表
async def get_categorise(db: AsyncSession,skip: int = 0,limit: int = 100):
    stmt = select(Categroy).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()