from fastapi import APIRouter

#创建router实例
router = APIRouter(prefix="/api/news",tags=["news"])
@router.get("/categorise")
#获取分类
async def categorise():
    return{"msg":"获取分类成功"}