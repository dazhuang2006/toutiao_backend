from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from pymilvus import MilvusClient

from llm.embeddings import embeddings
from llm.model import model

MILVUS_URI = "http://localhost:19530"
COLLECTION = "news_docs"

client = MilvusClient(MILVUS_URI)


def search_news(query: str, limit: int = 4) -> list[dict]:
    """在 Milvus 中检索与问题最相关的新闻片段"""
    vec = embeddings.embed_query(query)
    res = client.search(
        COLLECTION,
        data=[vec],
        limit=limit,
        output_fields=["news_id", "title", "text"],
    )
    return [hit["entity"] | {"score": hit["distance"]} for hit in res[0]]


def format_docs(docs: list[dict]) -> str:
    return "\n\n".join(f"[{d['title']}] {d['text']}" for d in docs)


QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "你是一名新闻助手。只能根据下面的资料回答，资料中没有的信息要明确说不知道，"
               "最后列出引用资料的标题。\n\n资料：\n{context}"),
    ("human", "问题：{question}"),
])

qa_chain = (
    {
        "context": itemgetter("question")
        | RunnableLambda(lambda q: format_docs(search_news(q))),
        "question": itemgetter("question"),
    }
    | QA_PROMPT
    | model
    | StrOutputParser()
)
