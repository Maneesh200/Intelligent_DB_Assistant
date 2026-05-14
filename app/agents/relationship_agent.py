from sqlalchemy import text
from database.db_connection import engine


def get_table_relationships():
    """
    Detect table relationships using:
    - common columns
    - probable foreign keys
    - join candidates
    """

    relationships = {}

    try:
        with engine.connect() as conn:

            # Get all business tables
            tables_query = text("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                ORDER BY name;
            """)

            tables_result = conn.execute(
                tables_query
            )

            tables = [
                row[0]
                for row in tables_result.fetchall()
                if row[0] not in [
                    "query_history",
                    "sqlite_sequence"
                ]
            ]

            table_columns = {}

            # Get columns of each table
            for table in tables:
                column_query = text(
                    f"PRAGMA table_info({table});"
                )

                result = conn.execute(column_query)

                columns = [
                    row[1]
                    for row in result.fetchall()
                ]

                table_columns[table] = columns

            # Detect relationships
            for table1 in tables:
                for table2 in tables:

                    if table1 != table2:

                        common_columns = list(
                            set(
                                table_columns[table1]
                            ).intersection(
                                set(
                                    table_columns[table2]
                                )
                            )
                        )

                        if common_columns:

                            relationships[
                                f"{table1} ↔ {table2}"
                            ] = common_columns

            return relationships

    except Exception as e:
        return {
            "error": str(e)
        }