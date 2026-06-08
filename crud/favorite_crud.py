from fastapi import Depends
from sqlalchemy import select
from sqlalchemy import delete, func, join
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.favorite_models import Favorite
from models.news_models import News


#检查收藏状态，检查当前用户是否收藏了该新闻
async def is_new_favorite(news_id:int,
                          user_id:int,
                         db:AsyncSession=Depends(get_db)):
   query=select(Favorite).where(Favorite.news_id==news_id,Favorite.user_id==user_id)
   result=await db.execute(query)
   #有没有收藏记录
   return result.scalar_one_or_none() is not None
#添加收藏
async def add_favorite(news_id:int,
                       user_id:int,
                       db:AsyncSession=Depends(get_db)):
    favorite=Favorite(news_id=news_id,user_id=user_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite
#取消收藏
async def remove_news_favorite(news_id:int,
                          user_id:int,
                          db:AsyncSession=Depends(get_db)):
    stmt=delete(Favorite).where(Favorite.news_id==news_id,Favorite.user_id==user_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
#获取收藏列表与分页功能
async def get_favorite_list(
        user_id:int,
        page:int=1,
        page_size:int=10,
        db:AsyncSession=Depends(get_db)
):
    #总量+收藏新闻列表
    count_query=select(func.count()).where(Favorite.user_id==user_id)
    count_result=await db.execute(count_query)
    total=count_result.scalar_one()
    offset=(page-1)*page_size
    query=(select(News, 
                  Favorite.created_at.label("favorite_time"),
                  Favorite.id.label("favorite_id"))
           .join(Favorite, Favorite.news_id==News.id)
           .where(Favorite.user_id==user_id)
           .order_by(Favorite.created_at.desc())
           .offset(offset).limit(page_size))
    result=await db.execute(query)
    rows=result.all()
    return rows,total

#清空新闻收藏列表
async def clear_favorite_list(user_id:int,
                              db:AsyncSession=Depends(get_db)):
    stmt=delete(Favorite).where(Favorite.user_id==user_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0



