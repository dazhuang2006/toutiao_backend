from models.news_models import Category
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.news_models import News

async def get_categorise(db: AsyncSession,skip: int = 0,limit: int = 100):
    stmt = select(Category).order_by(Category.sort_order).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

#查询指定分类下的新闻
async def get_news_list(
        db: AsyncSession,
        category_id: int,
        skip: int = 0,
        limit: int = 10
):
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()
#获取指定id新闻总量
async def get_news_count(db: AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)

    return result.scalar_one()
