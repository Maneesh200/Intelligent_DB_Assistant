from sqlalchemy import text
from database.db_connection import engine

def get_database_schema():
    schema_info = ""

    with engine.connect() as connection:
        tables_query = text("""
            SELECT name
            FROM sqlite_master
            WHERE type='table';
        """)

        tables = connection.execute(tables_query).fetchall()

        for table in tables:
            table_name = table[0]

            if table_name.startswith("sqlite_"):
                continue

            schema_info += f"\nTable: {table_name}\nColumns:\n"

            column_query = text(f"PRAGMA table_info({table_name});")
            columns = connection.execute(column_query).fetchall()

            for column in columns:
                column_name = column[1]
                column_type = column[2]

                schema_info += f"- {column_name} ({column_type})\n"

                # Fetch sample values for text columns
                if column_type.upper() in ["TEXT", "VARCHAR"]:
                    try:
                        sample_query = text(
                            f"SELECT DISTINCT {column_name} FROM {table_name} LIMIT 5;"
                        )
                        sample_values = connection.execute(sample_query).fetchall()

                        values = [str(v[0]) for v in sample_values if v[0] is not None]

                        if values:
                            schema_info += f"  Sample Values: {', '.join(values)}\n"

                    except:
                        pass

    return schema_info


if __name__ == "__main__":
    print(get_database_schema())