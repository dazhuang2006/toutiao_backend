from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy.sql.functions import user
from starlette import status

from crud import user_crud
from config.db_conf import get_db


#整合token查用户，返回用户
async def get_current_user(authorization: str = Header(...,alias="Authorization"),
                           db:AsyncSession=Depends(get_db)):
    token=authorization.split(" ")[1]
    user=await user_crud.get_user_by_token(token,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效或过期令牌")
    return user