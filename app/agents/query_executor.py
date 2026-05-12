from sqlalchemy import text
from app.database.db_connection import engine

def execute_query(sql_query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.fetchall()

            return rows

    except Exception as e:
        return f"Error: {str(e)}"