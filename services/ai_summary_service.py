from sqlalchemy.ext.asyncio import AsyncSession

from config.ai_conf import DEEPSEEK_MODEL
from config.cache_conf import (
    get_cache,
    set_cache,
)

from crud import ai_crud
from crud import news_crud

from llm.deepseek_client import deepseek_client
from utils.prompt_loader import prompt_loader


class AISummaryService:

    CACHE_EXPIRE = 60 * 60 * 24  # 24小时

    @staticmethod
    def _cache_key(news_id: int) -> str:
        """
        AI摘要缓存Key
        """
        return f"news:summary:{news_id}"

    async def get_summary(
        self,
        db: AsyncSession,
        news_id: int,
    ) -> str:
        """
        获取新闻AI摘要

        流程：
        Redis
            ↓
        MySQL
            ↓
        DeepSeek
            ↓
        MySQL
            ↓
        Redis
        """

        cache_key = self._cache_key(news_id)

        # =====================
        # 1.Redis
        # =====================
        cache = await get_cache(cache_key)

        if cache:
            return cache

        # =====================
        # 2.MySQL
        # =====================
        summary = await ai_crud.get_by_news_id(
            db=db,
            news_id=news_id,
        )

        if summary:

            await set_cache(
                cache_key,
                summary.summary,
                expire=self.CACHE_EXPIRE,
            )

            return summary.summary

        # =====================
        # 3.查询新闻
        # =====================
        news = await news_crud.get_news_detail(
            db=db,
            news_id=news_id,
        )

        if news is None:
            raise ValueError("新闻不存在")

        # =====================
        # 4.加载Prompt
        # =====================
        prompt = prompt_loader.load("summary")

        prompt = prompt.replace(
            "{{content}}",
            news.content,
        )

        # 如果Prompt中还有标题，可以放开
        # prompt = prompt.replace("{{title}}", news.title)

        # =====================
        # 5.调用AI
        # =====================
        summary_text = await deepseek_client.chat(prompt)

        # =====================
        # 6.保存数据库
        # =====================
        await ai_crud.create_summary(
            db=db,
            news_id=news.id,
            summary=summary_text,
            model_name=DEEPSEEK_MODEL,
        )

        # =====================
        # 7.写Redis
        # =====================
        await set_cache(
            cache_key,
            summary_text,
            expire=self.CACHE_EXPIRE,
        )

        return summary_text


ai_summary_service = AISummaryService()