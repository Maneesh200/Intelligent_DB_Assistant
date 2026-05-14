from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from agents.schema_agent import get_database_schema
import os
from agents.relationship_agent import get_table_relationships

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# prompt_template = PromptTemplate(
#     input_variables=["schema", "question"],
#     template="""
# You are an expert SQL assistant.

# Below is the live database schema:

# {schema}

# Rules:
# - Use only tables and columns from the schema above
# - Generate correct SQLite SQL query
# - For stock/count related questions, prefer SUM(quantity) when appropriate
# - Return ONLY SQL query
# - Do not explain anything

# User Question:
# {question}
# """
# )


prompt_template = PromptTemplate(
    input_variables=["schema", "relationships", "question"],
    template="""
You are an expert SQL assistant for dynamic business databases.

Your job is to generate ONLY valid SQLite SQL queries.

You must carefully analyze:
1. Database schema
2. Table relationships
3. User business question

and generate the best possible SQL query.

-----------------------------------
DATABASE SCHEMA
-----------------------------------

{schema}

-----------------------------------
TABLE RELATIONSHIPS
-----------------------------------

{relationships}

-----------------------------------
IMPORTANT RULES
-----------------------------------

1. Use ONLY tables and columns from the schema above

2. Use correct SQLite syntax only

3. Return ONLY SQL query

4. Do NOT explain anything

5. Do NOT use markdown

6. Do NOT write 'SQL Query:' before output

7. For stock / inventory questions:
   Prefer SUM(quantity) instead of COUNT(*)
   when quantity column exists

8. For ranking queries like:
   - highest
   - second highest
   - third highest
   - top N
   use proper ORDER BY / LIMIT / OFFSET / subqueries

9. For JOIN queries:
   Use table relationships intelligently

10. If multiple tables are involved:
   Prefer correct JOIN logic over assumptions

11. For NULL checks:
   Use IS NULL / IS NOT NULL
   never use = NULL

12. For date-based queries:
   Use proper SQLite date filtering

13. Always generate production-safe SQL

14. Never generate DELETE / DROP / TRUNCATE
   unless explicitly requested

15. If user asks for reports:
   use GROUP BY when required

-----------------------------------
USER QUESTION
-----------------------------------

{question}

-----------------------------------
FINAL OUTPUT
-----------------------------------

Return ONLY the SQL query.
"""
)


def generate_sql(question):
    # Get live database schema
    schema = get_database_schema()

    # Get table relationships
    relationship_info = get_table_relationships()

    # Build prompt using schema + relationships + question
    prompt = prompt_template.format(
        schema=schema,
        relationships=relationship_info,
        question=question
    )

    # Generate SQL using LLM
    response = llm.invoke(prompt)

    return response.content.strip()


if __name__ == "__main__":
    user_question = input("Ask your question: ")

    sql_query = generate_sql(user_question)

    print("\nGenerated SQL Query:")
    print(sql_query)