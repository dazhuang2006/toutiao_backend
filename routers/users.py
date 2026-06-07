from http.client import responses

from fastapi import HTTPException
from pyexpat.errors import messages
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.user_crud import get_user_by_username
from models.user_models import User
from schemas.news_sch import UserRequest, UserAuthResponse, UserInfoResponse
from crud import user_crud
from utils.auth import get_current_user
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
#用户登录
@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    user=await user_crud.authenticate_user(user_data.username,user_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token=await user_crud.create_token(user.id,db)
    responses_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate( user))
    return success_response(message="登录成功",data=responses_data)
#获取用户信息
@router.get("/info")
async def get_user_info(user:User=Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate( user))





