from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news_crud

#创建router实例
router = APIRouter(prefix="/api/news",tags=["news"])
@router.get("/categorise")
#获取分类
async def categorise(skip:int=0, limit:int=100,db:AsyncSession=Depends(get_db)):
    categories = await news_crud.get_categorise(db,skip, limit)
    return{
        "code":200,
        "message":" 获取新闻列表",
        "data":categories

    }