import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.embeddings import init_embeddings

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

EMBED_MODEL = "BAAI/bge-m3"
EMBED_DIM = 1024
#模型配置
embeddings = init_embeddings(
    model="openai:BAAI/bge-m3",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
    check_embedding_ctx_length=False,
)
