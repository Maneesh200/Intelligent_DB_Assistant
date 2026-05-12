from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from agents.schema_agent import get_database_schema
import os

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

prompt_template = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an expert SQL assistant.

Below is the live database schema:

{schema}

Rules:
- Use only tables and columns from the schema above
- Generate correct SQLite SQL query
- For stock/count related questions, prefer SUM(quantity) when appropriate
- Return ONLY SQL query
- Do not explain anything

User Question:
{question}
"""
)

def generate_sql(question):
    schema = get_database_schema()

    prompt = prompt_template.format(
        schema=schema,
        question=question
    )

    response = llm.invoke(prompt)
    return response.content.strip()


if __name__ == "__main__":
    user_question = input("Ask your question: ")
    sql_query = generate_sql(user_question)

    print("\nGenerated SQL Query:")
    print(sql_query)