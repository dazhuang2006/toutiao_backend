# 今日头条新闻系统后端（FastAPI）

基于 **FastAPI + MySQL + Redis** 构建的新闻资讯平台后端服务，提供完整的用户认证、新闻浏览、收藏管理、历史记录及缓存加速能力，采用异步架构设计，适合作为资讯类平台的后端基础框架。

---

## 项目简介

本项目实现了一个类似“今日头条”的新闻资讯平台核心后端功能，包括：

* 用户注册与登录
* Token 身份认证
* 新闻分类管理
* 新闻列表分页查询
* 新闻详情展示
* 新闻浏览量统计
* 新闻收藏与取消收藏
* 浏览历史管理
* Redis 热点数据缓存
* 全局异常处理

项目采用 FastAPI 异步开发模式，结合 MySQL 数据持久化与 Redis 缓存优化，提升系统响应性能与可扩展性。

---

## 技术栈

### 后端框架

* FastAPI
* Pydantic

### 数据库

* MySQL
* SQLAlchemy Async ORM
* aiomysql

### 缓存

* Redis
* redis-py asyncio

### 安全认证

* Token Authentication
* Passlib + Bcrypt

---

## 系统架构

```text
                Client
                   │
                   ▼
              FastAPI API
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
      Redis                MySQL
    （缓存层）            （数据层）
```

---

## 项目结构

```text
toutiao_backend/
├── cache/                # Redis缓存逻辑
├── config/               # 数据库与缓存配置
├── crud/                 # 数据库操作层
├── models/               # ORM模型
├── routers/              # API路由层
├── schemas/              # Pydantic数据模型
├── utils/                # 工具模块
├── main.py               # 项目入口
└── README.md
```

---

## 功能模块

### 用户模块

* 用户注册
* 用户登录
* Token生成与校验
* 获取用户信息
* 修改用户资料
* 修改密码

### 新闻模块

* 新闻分类查询
* 新闻分页列表
* 新闻详情查询
* 浏览量统计
* 相关新闻推荐

### 收藏模块

* 添加收藏
* 取消收藏
* 查询收藏状态
* 收藏列表分页
* 清空收藏

### 浏览历史模块

* 添加浏览记录
* 查询历史记录
* 删除单条记录
* 清空历史记录

---

## Redis缓存设计

为降低数据库访问压力，对热点数据进行缓存。

```text
# 新闻分类缓存
news:categories

# 新闻列表缓存
news_list:{category_id}:{page}:{size}

# 新闻详情缓存
news:detail:{news_id}

# 相关新闻缓存
news:related:{news_id}:{category_id}
```

缓存采用不同过期时间策略，减少缓存雪崩风险。

---

## 数据库设计

核心数据表：

| 表名            | 说明    |
| ------------- | ----- |
| user          | 用户表   |
| user_token    | 用户令牌表 |
| news_category | 新闻分类表 |
| news          | 新闻主表  |
| favorite      | 收藏表   |
| history       | 浏览历史表 |

---

## 快速启动

### 克隆项目

```bash
git clone https://github.com/yourname/toutiao_backend.git
cd toutiao_backend
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置数据库

修改：

```python
config/db_conf.py
```

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://用户名:密码@localhost:3306/news_app"
```

### 配置Redis

修改：

```python
config/cache_conf.py
```

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

### 启动项目

```bash
uvicorn main:app --reload
```

---

## API文档

启动后访问：

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## 项目亮点

* ✅ FastAPI 异步开发
* ✅ SQLAlchemy Async ORM
* ✅ Redis 缓存优化
* ✅ Token 用户认证
* ✅ RESTful API 设计
* ✅ Router / CRUD / Model / Schema 分层架构
* ✅ 全局异常处理机制
* ✅ 收藏与历史记录完整业务流程

---

## 后续优化方向

* JWT认证与刷新机制
* Docker / Docker Compose部署
* Nginx反向代理
* Elasticsearch全文检索
* 消息队列异步处理
* AI新闻摘要
* AI新闻问答
* 个性化推荐系统

---

## 作者
大壮
