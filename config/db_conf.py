from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession

#数据库URL
ASYNC_DATABASE_URL="mysql+aiomysql://root:3389485@localhost:3306/news_app"

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