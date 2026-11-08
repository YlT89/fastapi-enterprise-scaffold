import os
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# 1. 全局 Embedding 模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 2. 全局大语言模型
llm = init_chat_model(
    model="deepseek-flash",
    model_provider="openai",
    api_key=os.getenv("API_KEY"),
    base_url="https://api.deepseek.com"
)

# 3. 全局 Prompt 模板
prompt_template = """
请使用以下提供的文本内容来回答问题。仅使用提供的文本信息。
如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。

文本内容:
{context}

问题: {question}

回答:
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])