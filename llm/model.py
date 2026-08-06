import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


DeepSeek_API_KEY=os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL=os.getenv("DEEPSEEK_API_URL")
model=init_chat_model(
    model="deepseek:deepseek-v4-flash",
    api_base=DEEPSEEK_API_URL,
    api_key=DeepSeek_API_KEY
)
agent=create_agent(
    model=model,
    tools=[],
)
