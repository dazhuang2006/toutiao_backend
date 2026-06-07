from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_models import User
from schemas.news_sch import UserRequest
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