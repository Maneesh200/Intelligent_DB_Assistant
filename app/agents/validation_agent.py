def validate_sql_query(sql_query):
    """
    Validate SQL query before execution
    for safety and correctness
    """

    dangerous_keywords = [
        "delete",
        "drop",
        "truncate",
        "alter",
        "update",
        "insert"
    ]

    # Clean SQL safely
    cleaned_sql = sql_query.strip().lower()

    # Remove markdown if any
    cleaned_sql = cleaned_sql.replace("```sql", "")
    cleaned_sql = cleaned_sql.replace("```", "")
    cleaned_sql = cleaned_sql.replace("sql query:", "")
    cleaned_sql = cleaned_sql.strip()

    # Dangerous query detection
    for keyword in dangerous_keywords:
        if keyword in cleaned_sql:
            return (
                False,
                f"Unsafe SQL detected: '{keyword.upper()}' is not allowed."
            )

    # Allow only SELECT queries
    if not cleaned_sql.startswith("select"):
        return (
            False,
            "Only SELECT queries are allowed."
        )

    return (
        True,
        "SQL query is safe."
    )