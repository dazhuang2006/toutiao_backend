import asyncio

import models.news_models  # 注册 News 模型，避免 NewsAISummary 的 relationship 解析失败
from llm.summarizer import summarize


async def main():
    news_id = 1
    content = "这里随便放一段新闻正文，先用一句话测试。"
    result = await summarize(news_id=news_id, content=content)
    print(result)


asyncio.run(main())
