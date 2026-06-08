from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import user_crud, favorite_crud
from models.user_models import User
from schemas.favorite import FavoriteCheckRequest, FavoriteListResponse, FavoriteAddRequest
from utils.auth import get_current_user
from utils.response import success_response

router=APIRouter(prefix="/api/favorite",tags=["favorite"])


# 检查收藏
@router.get("/check")
async def check_favorite(news_id:int=Query( ...,alias="news_Id"),user:User=Depends(get_current_user),
                         db:AsyncSession=Depends(get_db)):
    is_favorite=await favorite_crud.is_new_favorite(news_id,user.id,db)
    return success_response(message="检查收藏成功",data=FavoriteCheckRequest(isFavorite=is_favorite))
#添加收藏
@router.post("/add")
async def add_favorite(data:FavoriteAddRequest,
                       user:User=Depends(get_current_user),
                       db:AsyncSession=Depends(get_db)):
    result=await favorite_crud.add_favorite(data.news_id,user.id,db)
    return success_response(message="添加收藏成功",data=result)
#取消收藏
@router.delete("/remove")
async def remove_favorite(news_id:int=Query( ...,alias="news_Id"),
                          user:User=Depends(get_current_user),
                          db:AsyncSession=Depends(get_db)):
    result=await favorite_crud.remove_news_favorite(news_id,user.id,db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="取消收藏失败")
    return success_response(message="取消收藏成功")
#获取收藏列表
@router.get("/list")
async def get_favorite_list(user:User=Depends(get_current_user),
                            page:int=Query(1,ge=1),
                            page_size:int=Query(10,ge=1,le=100,alias="pageSize"),
                            db:AsyncSession=Depends(get_db)):
    #收藏的新闻对象和总量(ORM)
    rows,total=await favorite_crud.get_favorite_list(user.id,page,page_size,db)
    favorite_list=[{
        **news.__dict__,
        "favorite_time":favorite_time,
        "favorite_id":favorite_id
    } for news,favorite_time,favorite_id in rows]
    has_more=total>page_size* page
    data=FavoriteListResponse(list=favorite_list,total=total,has_more=has_more)
    return success_response(message="获取收藏列表成功",data=data)

#清空收藏
@router.delete("/clear")
async def clear_favorite(user:User=Depends(get_current_user),
                         db:AsyncSession=Depends(get_db)):
    count=await favorite_crud.clear_favorite_list(user.id,db)
    return success_response(message=f"清空了{count}收藏")


