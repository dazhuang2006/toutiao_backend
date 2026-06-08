from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckRequest(BaseModel):
    is_favorite:bool=Field(...,alias="isFavorite",description="是否收藏")

#添加收藏
class FavoriteAddRequest(BaseModel):
    news_id:int=Field(...,alias="newsId",description="新闻id")



#收藏列表模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id:int=Field(...,alias="favoriteId",description="收藏id")
    favorite_time:datetime = Field(...,alias="favoriteTime",description="收藏时间")
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 模型对象属性中取值
        populate_by_name=True
    )


#收藏列表相应模型类
class FavoriteListResponse(BaseModel):
    list:list[FavoriteNewsItemResponse]
    total:int
    has_more:bool=Field(...,alias="hasMore",description="是否有更多")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 模型对象属性中取值
        populate_by_name=True
    )