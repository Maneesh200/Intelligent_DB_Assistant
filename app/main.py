from app.agents.sql_agent import generate_sql
from app.services.query_executor import execute_query

def main():
    user_question = input("Ask your business question: ")

    print("\nGenerating SQL query...")
    sql_query = generate_sql(user_question)

    print("\nGenerated SQL:")
    print(sql_query)

    print("\nExecuting query...")
    result = execute_query(sql_query)

    print("\nFinal Result:")
    print(result)

if __name__ == "__main__":
    main()