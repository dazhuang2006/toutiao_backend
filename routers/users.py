from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.user_crud import get_user_by_username
from schemas.news_sch import UserRequest
from crud import user_crud

router = APIRouter(prefix="/api/user",tags=["users"])
@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    existing_user=await get_user_by_username(user_data.username,db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user=await user_crud.create_user(user_data,db)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "令牌",
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }

