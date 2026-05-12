from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_business_response(user_question, sql_result):
    prompt = f"""
You are a business response assistant.

Convert the SQL output into a professional,
clear, human-friendly business answer.

User Question:
{user_question}

SQL Result:
{sql_result}

Return only final business answer.
Do not explain technical details.
"""

    response = llm.invoke(prompt)
    return response.content.strip()