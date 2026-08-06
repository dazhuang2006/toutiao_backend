from pymilvus import MilvusClient

from llm.embeddings import embeddings

client = MilvusClient("http://localhost:19530")

query_vec = embeddings.embed_query("哪篇新闻提到了芯片量产")
res = client.search(
    "news_docs",
    data=[query_vec],
    limit=4,
    output_fields=["news_id", "title", "text"],
)

for hit in res[0]:
    print(hit["entity"]["title"], hit["distance"])