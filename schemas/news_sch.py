from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
#from typing_inspection.typing_objects import alias


class UserRequest(BaseModel):
    username: str
    password: str
#user_info对应类
# user_info 对应的类：基础类 + Info 类（id、用户名）
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 对象属性中取值
    )



#data数据类型
class UserAuthResponse(BaseModel):
    token:str
    user_info: UserInfoResponse =Field(...,alias="userInfo")

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes= True
    )
#更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname:Optional[str]=None
    avatar:Optional[str]=None
    gender:Optional[str]=None
    bio:Optional[str]=None
    phone:Optional[str]=None
#修改密码模型类
class UserUpdatePasswordRequest(BaseModel):
    old_password:str=Field(...,alias="oldPassword",description="旧密码")
    new_password:str=Field(...,min_length=6,max_length=20,alias="newPassword",description="新密码")
