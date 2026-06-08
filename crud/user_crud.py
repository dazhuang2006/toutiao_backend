import uuid
from datetime import datetime, timedelta
from email import utils

from fastapi import HTTPException
from starlette import status

from utils import secrity
from utils.secrity import verify_password
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_models import User, UserToken
from schemas.news_sch import UserRequest, UserUpdateRequest
from utils.secrity import get_password_hash


#用户名查数据库
async def get_user_by_username(username:str,db:AsyncSession):
    stmt=select(User).where(User.username==username)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()
#创建用户
async def create_user(user_data:UserRequest,db:AsyncSession):
    hashed_password=get_password_hash(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) #刷新回读，在数据库获取新数据
    return user
#创建token
async def create_token(user_id:int,db:AsyncSession):
    #生成token+过期时间，查询数据库有没有
    token=str(uuid.uuid4())
    expires_at=datetime.now()+timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token
#验证用户
async def authenticate_user(username:str,password:str,db:AsyncSession):
    user=await get_user_by_username(username,db)
    if not user:
        return None
    if not verify_password(password,user.password):
        return None
    return user
#根据token查用户
async def get_user_by_token(token:str,db:AsyncSession):
    query=select(UserToken).where(UserToken.token==token)
    result=await db.execute(query)
    db_token=result.scalar_one_or_none()
    if not db_token or db_token.expires_at<datetime.now():
        return None
    query=select(User).where(User.id==db_token.user_id)
    result=await db.execute(query)
    return result.scalar_one_or_none()
#更新用户信息
async def update_user(user_data:UserUpdateRequest,username:str,db:AsyncSession):
    query=update(User).where(User.username==username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result=await db.execute(query)
    await db.commit()
    #检查更新,是否命中
    if result.rowcount ==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="用户不存在")
    #获取用户更新结果
    update_user=await get_user_by_username(username,db)
    return update_user
#更新用户密码,验证旧密码,弄新密码加密，提交
async def change_password(old_password:str,new_password:str,user: User,db:AsyncSession):
    if not verify_password(old_password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="旧密码错误")
    hashed_new_password=secrity.get_password_hash(new_password)
    user.password=hashed_new_password
    #由SQLAlchemy接管User对象，确保可以commit
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True

