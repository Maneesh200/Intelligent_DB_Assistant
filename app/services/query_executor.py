# from sqlalchemy import text
# from database.db_connection import engine


# def execute_query(sql_query):
#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text(sql_query))
#             rows = result.fetchall()

#             if not rows:
#                 return "No data found."

#             # If single numeric result like COUNT / SUM
#             if len(rows) == 1 and len(rows[0]) == 1:
#                 value = rows[0][0]

#                 if value is None:
#                     return "No matching records found."

#                 return f"{value} records found."

#             return str(rows)

#     except Exception as e:
#         return f"Error: {str(e)}"


from sqlalchemy import text
from database.db_connection import engine


def execute_query(sql_query):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(sql_query)
            )

            rows = result.fetchall()

            return rows

    except Exception as e:
        return f"Error: {str(e)}"