from fastapi import Query

from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news_crud

#模块化路由
router = APIRouter(prefix="/api/news",tags=["news"])
# 获取新闻分类列表
@router.get("/categorise")
async def categorise(skip:int=0, limit:int=100,db:AsyncSession=Depends(get_db)):
    categories = await news_crud.get_categorise(db,skip,limit)
    return {
        "code":200,
        "message":"获取新闻分类列表",
        "data":categories

    }
#获取新闻列表
@router.get("/list")
async def get_news(
        category_id:int=Query(...,alias="categoryId"),  #驼峰命名方便前端
        page:int=1,
        page_size:int=Query(10,le=100,alias="pageSize"),
        db:AsyncSession=Depends(get_db)
):
    #指定id查询并且分页处理
    offset=(page-1)*page_size
    new_list=await news_crud.get_news_list(db,category_id,offset,page_size)
    #获取新闻总数
    total=await news_crud.get_news_count(db,category_id)
    #是否还有更多新闻
    has_more=(offset+len(new_list))<total

    return{
        "code":200,
        "message":"success",
        "data":{
            "list":new_list,
            "total":total,
            "hasMore":has_more
        }
    }
