from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()
# 注册异常处理
register_exception_handlers(app)

#跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
#注册router路由
app.include_router(news.router)
app.include_router(users.router)

