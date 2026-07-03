FROM python:3.11-slim

WORKDIR /app

# 防止 Python 缓存 & 日志问题
ENV PYTHONUNBUFFERED=1

# 安装系统依赖（MySQL / cryptography 常见依赖）
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 先复制 requirements（利用 Docker 缓存）
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 再复制项目代码
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]