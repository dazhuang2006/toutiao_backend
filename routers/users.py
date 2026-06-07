from http.client import responses

from fastapi import HTTPException
from pyexpat.errors import messages
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.user_crud import get_user_by_username
from schemas.news_sch import UserRequest, UserAuthResponse, UserInfoResponse
from crud import user_crud
from utils.response import success_response

router = APIRouter(prefix="/api/user",tags=["users"])
@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    existing_user=await get_user_by_username(user_data.username,db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user=await user_crud.create_user(user_data,db)
    token=await user_crud.create_token(user.id,db)
    responses_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate( user))
    return success_response(message="注册成功",data=responses_data)
    '''

    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": user.id,
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }
'''


