import asyncio
import sys

from llm.rag import qa_chain, search_news

sys.stdout.reconfigure(encoding="utf-8")


async def main():
    question = "量子通信有什么最新进展？"
    print("问题:", question)

    docs = search_news(question)
    print("\n检索来源:")
    for d in docs:
        print("-", d["title"], round(d["score"], 4))

    answer = await qa_chain.ainvoke({"question": question})
    print("\n回答:\n", answer)


asyncio.run(main())
