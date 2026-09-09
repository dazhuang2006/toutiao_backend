from langchain.chat_models import init_chat_model

from config.ai_conf import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL

MODEL_NAME = f"deepseek:{DEEPSEEK_MODEL}"

model = init_chat_model(
    model=MODEL_NAME,
    api_base=DEEPSEEK_API_URL,
    api_key=DEEPSEEK_API_KEY,
)
