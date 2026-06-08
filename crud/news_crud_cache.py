from fastapi.encoders import jsonable_encoder
from sqlalchemy import update

from cache.news_cache import get_cached_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from config.cache_conf import get_cache
from models.news_models import Category
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.news_models import News
from schemas.base import NewsItemBase


async def get_categorise(db: AsyncSession,skip: int = 0,limit: int = 100):
    #尝试缓存获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories
    stmt = select(Category).order_by(Category.sort_order).offset(skip).limit(limit)
    result=await db.execute(stmt)
    categories= result.scalars().all()
    #写入缓存
    if categories:#categories是ORM对象,需要转换成字典
        categories=jsonable_encoder( categories)
        await set_cache_categories(categories)
    #返回数据
    return categories

#查询指定分类下的新闻
async def get_news_list(
        db: AsyncSession,
        category_id: int,
        skip: int = 0,
        limit: int = 10
):
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    #缓存获取新闻
    #页码
    page=skip// limit+1

    #分类id，页码，每页数量
    cached_list=await get_cache_news_list(category_id, page, limit)
    if cached_list:
        #return cached_list 这个返回的是JSON，要的是ORM
        return [News(**item)for item in cached_list]
    result=await db.execute(stmt)
    news_list = result.scalars().all()
    #写入缓存
    if news_list:
        #news_list=jsonable_encoder(news_list)要把ORM转成字典
        news_data = [NewsItemBase.model_validate(item)
                     .model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)



    return news_list
#获取指定id新闻总量
async def get_news_count(db: AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one()
#获取指定id新闻详情
async def get_news_detail(db: AsyncSession,news_id:int):
    stmt=select(News).where(News.id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()
#更新指定id新闻浏览量
async def update_news_views(db: AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views+1)
    result= await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
#获取同类推荐新闻
async def get_related_news(db: AsyncSession,news_id:int,category_id:int,limit:int=5):
    stmt=select(News).where(News.category_id==category_id,News.id!=news_id
                        ).order_by(News.views.desc()#降序,默认是升序
                                   ).limit(limit)#返回5个
    result=await db.execute(stmt)
    related_new = result.scalars().all()
    #返回新闻的核心数据
    return[{
        "id": news_detail.id,
        "title": news_detail.title,
        "description": news_detail.description,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "publishTime": news_detail.publish_time
    }for news_detail in related_new]
