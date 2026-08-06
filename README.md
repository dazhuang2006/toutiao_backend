# 今日头条新闻系统（toutiao_backend）

基于 **FastAPI + MySQL + Redis + LangChain / DeepSeek + Milvus** 的新闻资讯平台，提供用户认证、新闻浏览、收藏管理、浏览历史、Redis 缓存、AI 新闻摘要、RAG 新闻问答与 Agent 新闻助手能力。前端使用 Vue 3 + Vite，并采用 The Verge 风格设计语言；后端异步架构设计，适合作为资讯类平台的学习与基础框架项目。

---

## 功能特性

### 用户模块

- 用户注册 / 登录
- Token 身份认证（注册登录后返回 `token`，有效期 7 天）
- 获取用户信息、修改资料、修改密码

### 新闻模块

- 新闻分类列表
- 新闻分页列表
- 新闻详情（浏览量 +1）
- 相关新闻推荐
- AI 新闻摘要

### AI 能力（LangChain + DeepSeek + Milvus）

- AI 摘要：`PromptTemplate | ChatDeepSeek | StrOutputParser`
  - 多级缓存：Redis 命中 → MySQL 命中 → 调用大模型 → 写库 → 回填 Redis
  - Redis 不可用时自动降级，不影响摘要生成
- RAG 新闻问答：新闻切块向量化存入 Milvus，检索相关片段后由 DeepSeek 生成带来源的回答
- Agent 新闻助手：`create_agent` 封装检索与摘要工具，自动决定调用方式

### 收藏模块

- 检查收藏状态、添加 / 取消收藏
- 收藏列表分页、清空收藏

### 浏览历史模块

- 添加浏览记录、历史列表分页
- 删除单条记录、清空历史

### 工程能力

- Redis 热点数据缓存（分类 / 列表 / 详情 / 相关新闻 / AI 摘要）
- 全局异常处理（HTTP、数据库约束、SQLAlchemy、通用异常）
- FastAPI 自动 API 文档（Swagger / ReDoc）

---

## 技术栈

| 分类 | 技术 |
| --- | --- |
| 后端框架 | FastAPI、Pydantic |
| 数据库 | MySQL 8、SQLAlchemy 2 Async ORM、aiomysql |
| 缓存 | Redis 7、redis-py asyncio |
| 安全认证 | Token Authentication、Passlib + Bcrypt |
| AI 能力 | LangChain 1.x、langchain-deepseek、DeepSeek API、SiliconFlow BGE-M3 |
| 向量库 | Milvus、pymilvus |
| 前端 | Vue 3、Vite、Vue Router、Axios（The Verge 风格设计） |
| 部署 | Uvicorn、Docker Compose |

---

## 目录结构

```text
toutiao_backend/
├── cache/                   # Redis 缓存逻辑
├── config/                  # 数据库、Redis、AI 配置
├── crud/                    # 数据库操作层
├── frontend/                # Vue 3 前端
├── llm/                     # LangChain AI 能力
│   ├── model.py             # ChatDeepSeek 模型初始化
│   ├── embeddings.py        # SiliconFlow BGE-M3 向量模型
│   ├── summarizer.py        # 摘要链路（Redis + MySQL + DeepSeek）
│   ├── rag.py               # Milvus 检索 + RAG 问答链
│   ├── agent.py             # create_agent 新闻助手
│   └── index_news.py        # 新闻向量索引脚本
├── models/                  # SQLAlchemy ORM 模型
├── prompts/                 # Prompt 文本模板（预留）
├── routers/                 # API 路由层
│   ├── news.py              # 新闻相关接口
│   ├── ai_summary_router.py # AI 摘要 / RAG 问答 / Agent 接口
│   ├── users.py             # 用户接口
│   ├── favorite.py          # 收藏接口
│   └── history.py           # 历史记录接口
├── schemas/                 # Pydantic 数据模型
│   └── ask_sch.py           # AI 问答请求体
├── services/                # 独立服务 / 测试脚本
│   ├── test_summary.py      # AI 摘要本地测试
│   ├── qa_demo.py           # RAG 问答本地测试
│   └── agent_demo.py        # Agent 本地测试
├── utils/                   # 工具模块（认证、响应、异常处理）
├── main.py                  # FastAPI 入口
├── requirements.txt         # Python 依赖
├── docker-compose.yml       # Docker 编排
└── Dockerfile
```

---

## 快速开始

### 1. 环境准备

- Python 3.11+
- MySQL 8（或直接使用下面的 Docker Compose）
- Redis 7
- Milvus（RAG 功能需要，默认连接 http://localhost:19530）
- Node.js 18+（仅前端开发时需要）

### 2. 配置环境变量

复制环境变量模板并填写：

```bash
cp .env.example .env
```

至少需要配置 MySQL、Redis 和 DeepSeek：

```dotenv
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=news_app

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com

SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_API_KEY=your_siliconflow_api_key
```

> 注意：代码实际读取的键名是 `DEEPSEEK_API_URL`（见 `config/ai_conf.py`），`.env.example` 中旧的 `DEEPSEEK_BASE_URL` 建议统一改为 `DEEPSEEK_API_URL`。
> RAG 新闻问答使用硅基流动 SiliconFlow 的 `BAAI/bge-m3` 向量模型，需要配置 `SILICONFLOW_BASE_URL` 与 `SILICONFLOW_API_KEY`。

### 3. 创建虚拟环境并安装依赖

Windows：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> 本项目强烈建议始终使用项目内的 `.venv`，不要使用全局 pip，避免依赖装错环境。

### 4. 初始化数据库

项目启动前需要保证数据表存在。可以在项目根目录临时执行：

```python
import asyncio

import models.ai_summary
import models.favorite_models
import models.history_models
import models.news_models
import models.user_models
from config.db_conf import engine
from models.base import Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_db())
```

核心数据表：

| 表名 | 说明 |
| --- | --- |
| user | 用户表 |
| user_token | 用户令牌表 |
| news_category | 新闻分类表 |
| news | 新闻主表 |
| favorite | 收藏表 |
| history | 浏览历史表 |
| news_ai_summary | AI 摘要表（`news_id` 唯一） |

### 5. 启动 Milvus 并建立新闻向量索引

RAG 问答需要 Milvus 服务。可以使用课程资料中的 `standalone.bat`，或自行启动 Milvus standalone：

```bash
docker run -d --name milvus-standalone \
  -p 19530:19530 -p 9091:9091 \
  milvusdb/milvus:latest milvus run standalone
```

Milvus 就绪后，执行索引脚本，将 MySQL 中的新闻切块、向量化并写入 `news_docs` 集合：

```bash
.\.venv\Scripts\python -m llm.index_news
```

> 首次运行会调用 SiliconFlow embedding 接口；新闻内容变化后需要重新执行索引。学习阶段可以删除集合后重建。

### 6. 启动后端

```bash
uvicorn main:app --reload
```

启动后访问：

- 健康检查：http://127.0.0.1:8000/api/health
- Swagger 文档：http://127.0.0.1:8000/docs
- ReDoc 文档：http://127.0.0.1:8000/redoc

### 7. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器运行在 http://localhost:5173，`/api` 请求会自动代理到后端 8000 端口。
界面采用 The Verge 风格设计：近黑画布、酸性薄荷绿 / 紫外紫强调色、1px 细边框与饱和色新闻卡片。

也可以先构建前端，再由 FastAPI 直接托管静态文件：

```bash
cd frontend
npm run build
```

构建产物位于 `frontend/dist`，后端检测到该目录后会自动挂载。

---

## 环境变量说明

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| DB_USER | 是 | MySQL 用户名 |
| DB_PASSWORD | 是 | MySQL 密码 |
| DB_HOST | 是 | MySQL 地址，默认 localhost |
| DB_PORT | 是 | MySQL 端口，默认 3306 |
| DB_NAME | 是 | 数据库名，默认 news_app |
| REDIS_HOST | 是 | Redis 地址，默认 localhost |
| REDIS_PORT | 是 | Redis 端口，默认 6379 |
| REDIS_DB | 是 | Redis 数据库编号，默认 0 |
| DEEPSEEK_API_KEY | 是 | DeepSeek API Key |
| DEEPSEEK_API_URL | 否 | DeepSeek API 地址，默认 https://api.deepseek.com |
| DEEPSEEK_MODEL | 否 | 模型名，默认 deepseek-chat（`llm/model.py` 当前硬编码了实际使用的模型） |
| SILICONFLOW_BASE_URL | 否（RAG 需要） | SiliconFlow 接口地址，默认 https://api.siliconflow.cn/v1 |
| SILICONFLOW_API_KEY | 否（RAG 需要） | SiliconFlow API Key，RAG 向量化使用 |
| JWT_SECRET_KEY 等 | 否 | 预留配置，当前认证使用数据库 token 表 |

---

## API 接口

统一响应格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

需要登录的接口在请求头携带：

```text
Authorization: Bearer <token>
```

### 用户模块

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| POST | /api/user/register | 注册 | 否 |
| POST | /api/user/login | 登录 | 否 |
| GET | /api/user/info | 获取用户信息 | 是 |
| PUT | /api/user/update | 修改用户资料 | 是 |
| PUT | /api/user/update_password | 修改密码 | 是 |

### 新闻模块

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| GET | /api/news/categorise?skip=0&limit=100 | 新闻分类列表 | 否 |
| GET | /api/news/list?categoryId=1&page=1&pageSize=10 | 新闻分页列表 | 否 |
| GET | /api/news/detail?id=1 | 新闻详情（含 AI 摘要） | 否 |
| GET | /api/news/ai-summary?id=1 | 单独获取 AI 摘要 | 否 |
| POST | /api/news/ask | RAG 新闻问答，body：`{"question": "..."}`，返回回答与来源 | 否 |
| POST | /api/news/agent | Agent 新闻助手问答，body：`{"question": "..."}` | 否 |

### 收藏模块

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| GET | /api/favorite/check?news_Id=1 | 检查是否已收藏 | 是 |
| POST | /api/favorite/add | 添加收藏，body：`{"newsId": 1}` | 是 |
| DELETE | /api/favorite/remove?news_Id=1 | 取消收藏 | 是 |
| GET | /api/favorite/list?page=1&pageSize=10 | 收藏列表 | 是 |
| DELETE | /api/favorite/clear | 清空收藏 | 是 |

### 历史记录模块

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| POST | /api/history/add | 添加记录，body：`{"newsId": 1}` | 是 |
| GET | /api/history/list?page=1&pageSize=10 | 历史列表 | 是 |
| DELETE | /api/history/delete/{history_id} | 删除单条记录 | 是 |
| DELETE | /api/history/clear | 清空历史 | 是 |

---

## AI 能力设计

### AI 摘要

摘要链路位于 `llm/summarizer.py`，核心是 LangChain 链：

```text
PromptTemplate | ChatDeepSeek | StrOutputParser
```

调用顺序：

```text
1. Redis 查询 news:summary:{news_id}
2. 未命中 → MySQL 查询 news_ai_summary
3. 仍未命中 → 调用 DeepSeek 生成摘要
4. 写入 MySQL
5. 回填 Redis（24 小时过期）
```

设计说明：

- 缓存 key：`news:summary:{news_id}`
- 摘要结果以 `news_id` 为唯一键持久化，重复请求不会重复调用大模型
- Redis 不可用时 `get_cache` / `set_cache` 自动降级，只会打印错误日志，不影响接口
- 模型配置在 `llm/model.py`，当前使用 `deepseek:deepseek-v4-flash`，请以 DeepSeek 官方实际支持的模型名为准

本地测试摘要：

```bash
# 需要在项目根目录执行
.\.venv\Scripts\python -m services.test_summary
```

### RAG 新闻问答

链路位于 `llm/rag.py`：

```text
问题 → Milvus 检索相关片段 → 拼 context → ChatPromptTemplate → DeepSeek → 回答 + 来源
```

- 新闻向量索引：`llm/index_news.py`（MySQL → 切块 → SiliconFlow BGE-M3 → Milvus）
- 向量集合：`news_docs`，1024 维，余弦相似度
- 接口：`POST /api/news/ask`

本地测试问答：

```bash
.\.venv\Scripts\python -m services.qa_demo
```

### Agent 新闻助手

链路位于 `llm/agent.py`，使用 `create_agent` 封装工具：

- `search_news_tool`：在 Milvus 中检索新闻片段
- `get_news_summary_tool`：按新闻 ID 获取 AI 摘要
- 接口：`POST /api/news/agent`

本地测试 Agent：

```bash
.\.venv\Scripts\python -m services.agent_demo
```

---

## Redis 缓存设计

| Key | 说明 |
| --- | --- |
| news:categories | 新闻分类缓存 |
| news_list:{category_id}:{page}:{size} | 新闻列表缓存 |
| news:detail:{news_id} | 新闻详情缓存 |
| news:related:{news_id}:{category_id} | 相关新闻缓存 |
| news:summary:{news_id} | AI 摘要缓存 |

---

## Docker 部署

仓库已提供 `Dockerfile` 和 `docker-compose.yml`，包含后端、MySQL、Redis 三个服务：

```bash
cp .env.example .env
docker compose up -d --build
```

| 服务 | 对外端口 | 说明 |
| --- | --- | --- |
| backend | 8000 | FastAPI 应用 |
| mysql | 3307 | MySQL 8，宿主机端口为 3307 |
| redis | 6379 | Redis 7 |

> RAG 使用的 Milvus 不在 compose 中，需要单独启动（见“快速开始”）。

---

## 常见问题

**1. 为什么 `pip install` 装完项目里还是找不到 langchain？**

控制台默认 `pip` 可能指向全局 conda / 系统 Python，而不是项目 `.venv`。请使用：

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

**2. Redis 没启动会怎样？**

新闻浏览不受影响；AI 摘要会跳过缓存直接生成，日志会打印连接失败，但接口仍然可用。

**3. 数据库表不存在怎么办？**

使用上文“初始化数据库”中的脚本建表，或导入已有的 SQL 文件。

**4. DeepSeek 调用报错？**

确认 `.env` 中的 `DEEPSEEK_API_KEY` 和 `DEEPSEEK_API_URL` 正确，并确认模型名在 DeepSeek 官方接口中可用。

**5. 向量检索结果不准？**

确认 `llm/embeddings.py` 中设置了 `check_embedding_ctx_length=False`。langchain-openai 默认开启 tiktoken 长度检查，会把 token id 发给硅基流动，导致向量没有语义。

**6. Milvus 连接被拒（localhost:19530）？**

Milvus 服务没有启动。先启动 Milvus，再执行 `llm.index_news` 和问答接口。

**7. 搜不到 `news_docs` 集合？**

还没有成功执行 `python -m llm.index_news`。确认 `.env` 中 `SILICONFLOW_API_KEY` 已配置，Milvus 已启动，然后重新执行索引。

---

## 作者

大壮
