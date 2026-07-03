from tkinter.constants import NORMAL

from sqlalchemy import (Column,BigInteger,String,Text,
DateTime,SmallInteger,ForeignKey,func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class SummaryStatus:
    NORMAL = 1
    FAIL = 2
    GENERATING = 0
class Base(DeclarativeBase):
    pass

class NewsAISummary(Base):
    __tablename__ = "news_ai_summary"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    news_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("news.id"),
                                         nullable=False,unique= True,index= True,comment="新闻ID")
    summary: Mapped[str] = mapped_column(Text, nullable=False,comment="新闻摘要")
    model_name: Mapped[str] = mapped_column(String(50), nullable=False,comment="模型名称")
    prompt_version: Mapped[str] = mapped_column(String(50), nullable=False,comment="模型版本")
    status: Mapped[int] = mapped_column(SmallInteger, default=NORMAL,comment="状态")#1:正常 2:失败 0:生成中
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(),comment="创建时间")
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(),comment="更新时间")
    nwes=relationship("News",back_populates="summary")#relationship