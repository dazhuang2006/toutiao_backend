import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient
from sqlalchemy import select

from config.db_conf import AsyncSessionLocal
from llm.embeddings import EMBED_DIM, embeddings
import models.ai_summary  # 注册 NewsAISummary，让 News 的 relationship 能解析
from models.news_models import News

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MILVUS_URI = "http://localhost:19530"
COLLECTION = "news_docs"


async def load_news():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(News))
        return result.scalars().all()


def build_docs(news_list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=220,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    )
    docs = []
    for news in news_list:
        if not news.content:
            continue
        for i, chunk in enumerate(splitter.split_text(news.content)):
            docs.append({
                "news_id": news.id,
                "title": news.title,
                "category_id": news.category_id,
                "text": chunk,
                "chunk_index": i,
            })
    return docs


async def main():
    news_list = await load_news()
    docs = build_docs(news_list)
    print(f"新闻数: {len(news_list)}, 块数: {len(docs)}")

    vectors = embeddings.embed_documents([d["text"] for d in docs])

    client = MilvusClient(MILVUS_URI)
    if not client.has_collection(COLLECTION):
        client.create_collection(
            collection_name=COLLECTION,
            dimension=EMBED_DIM,
            metric_type="COSINE",
            enable_dynamic_field=True,
        )

    rows = [
        {"id": i + 1, "vector": vec, **doc}
        for i, (doc, vec) in enumerate(zip(docs, vectors))
    ]
    client.insert(collection_name=COLLECTION, data=rows)
    print("索引完成")


if __name__ == "__main__":
    asyncio.run(main())
