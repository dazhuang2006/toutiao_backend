import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession

# 加载环境变量
load_dotenv()

#数据库URL - 从环境变量读取
DATABASE_USER = os.getenv("DB_USER", "root")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD", "")
DATABASE_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_PORT = os.getenv("DB_PORT", "3306")
DATABASE_NAME = os.getenv("DB_NAME", "news_app")

ASYNC_DATABASE_URL=f"mysql+aiomysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

#异步引擎
engine=create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    connect_args={"charset": "utf8mb4"}
)

#异步会话
AsyncSessionLocal=async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()