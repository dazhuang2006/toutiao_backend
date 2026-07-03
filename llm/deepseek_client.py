from openai import AsyncOpenAI, AuthenticationError, APITimeoutError, RateLimitError, APIConnectionError

from config.ai_conf import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
)


class DeepSeekClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )

    async def chat(self, prompt: str, temperature: float = 0.3) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
            )
            return response.choices[0].message.content
        except AuthenticationError:
            raise RuntimeError("DeepSeek API Key 无效")
        except APITimeoutError:
            raise RuntimeError("DeepSeek 请求超时")
        except RateLimitError:
            raise RuntimeError("DeepSeek 请求过于频繁")
        except APIConnectionError:
            raise RuntimeError("无法连接 DeepSeek 服务")
        except Exception as e:
            raise RuntimeError(f"AI 摘要生成失败：{str(e)}")


# 实例化
deepseek_client = DeepSeekClient()
