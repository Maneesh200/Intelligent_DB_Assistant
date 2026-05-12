from datetime import datetime
import matplotlib.pyplot as plt
from sqlalchemy import text
import pandas as pd
from database.db_connection import engine


def create_dynamic_table(table_name, columns):
    """
    Create a new table dynamically from UI input.
    Example:
    table_name = customers
    columns = customer_name, revenue, city
    """
    try:
        formatted_columns = ", ".join(
            [f"{col.strip()} TEXT" for col in columns.split(",")]
        )

        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {formatted_columns}
        );
        """

        with engine.connect() as connection:
            connection.execute(text(create_query))
            connection.commit()

        return f"Table '{table_name}' created successfully!"

    except Exception as e:
        return f"Error while creating table: {str(e)}"



def delete_table(table_name):
    """
    Delete an existing table dynamically from UI input.
    Example:
    table_name = products
    """
    try:
        if not table_name or not table_name.strip():
            return "Please provide a valid table name"

        drop_query = f"DROP TABLE IF EXISTS {table_name};"

        with engine.connect() as connection:
            connection.execute(text(drop_query))
            connection.commit()

        return f"Table '{table_name}' deleted successfully!"

    except Exception as e:
        return f"Error while deleting table: {str(e)}"
    


def upload_csv_to_db(uploaded_file, table_name):
    """
    Upload CSV file and insert data into SQLite table
    """

    try:
        # Reset file pointer to start
        uploaded_file.seek(0)

        df = pd.read_csv(uploaded_file)

        df.to_sql(
            table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

        return f"CSV uploaded successfully to table '{table_name}'!"

    except Exception as e:
        return f"Error while uploading CSV: {str(e)}"
    


def get_all_tables():
    """
    Fetch only business tables from SQLite
    Hide internal/system tables
    """

    try:
        with engine.connect() as conn:
            query = text("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                ORDER BY name;
            """)

            result = conn.execute(query)
            all_tables = [
                row[0]
                for row in result.fetchall()
            ]

            # Tables we want to hide
            excluded_tables = [
                "query_history",
                "sqlite_sequence"
            ]

            filtered_tables = [
                table
                for table in all_tables
                if table not in excluded_tables
            ]

            return filtered_tables

    except Exception:
        return []
    


def preview_table_data(table_name):
    """
    Fetch preview of selected table
    """

    try:
        query = f"SELECT * FROM {table_name} LIMIT 10"
        df = pd.read_sql(query, engine)
        return df

    except Exception as e:
        return pd.DataFrame()
    




def generate_basic_analytics(table_name):
    """
    Auto-generate analytics charts
    """

    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)

        return df

    except Exception as e:
        return pd.DataFrame()
    



def save_query_history(user_question, generated_sql, final_result):
    """
    Save query history into database
    """

    try:
        create_history_table = """
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_question TEXT,
            generated_sql TEXT,
            final_result TEXT,
            created_at TEXT
        )
        """

        insert_query = """
        INSERT INTO query_history (
            user_question,
            generated_sql,
            final_result,
            created_at
        )
        VALUES (
            :user_question,
            :generated_sql,
            :final_result,
            :created_at
        )
        """

        with engine.connect() as conn:
            conn.execute(text(create_history_table))

            conn.execute(
                text(insert_query),
                {
                    "user_question": user_question,
                    "generated_sql": generated_sql,
                    "final_result": str(final_result),
                    "created_at": str(datetime.now())
                }
            )

            conn.commit()

        return "History saved successfully"

    except Exception as e:
        return f"Error saving history: {str(e)}"