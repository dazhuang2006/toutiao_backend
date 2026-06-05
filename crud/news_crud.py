from models.news_models import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_categorise(db: AsyncSession,skip: int = 0,limit: int = 100):
    stmt = select(Category).order_by(Category.sort_order).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()