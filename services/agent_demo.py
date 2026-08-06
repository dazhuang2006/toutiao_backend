import asyncio
import sys

from llm.agent import news_agent

sys.stdout.reconfigure(encoding="utf-8")


async def main():
    question = "量子通信有什么最新进展？帮我总结一篇相关新闻。"
    print("问题:", question)

    result = await news_agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    print("\n回答:\n", result["messages"][-1].content)


asyncio.run(main())
