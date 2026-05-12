from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""
You are an expert SQL assistant.

Convert the following user question into a correct MySQL SQL query.

Only return SQL query.
Do not explain anything.

User Question:
{question}
"""
)

def generate_sql(question):
    prompt = prompt_template.format(question=question)
    response = llm.invoke(prompt)
    return response.content.strip()


if __name__ == "__main__":
    user_question = input("Ask your question: ")
    sql_query = generate_sql(user_question)

    print("\nGenerated SQL Query:")
    print(sql_query)