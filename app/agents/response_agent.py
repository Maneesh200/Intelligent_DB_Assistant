from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_business_response(
    question,
    sql_query,
    query_result
):
    """
    SQL-Aware Universal Response Agent

    Uses:
    - SQL Query
    - Actual DB Result

    Handles:
    - count
    - sum
    - average
    - max / min
    - difference calculations
    - text results
    - single row / single value
    - multiple rows
    - single-column multiple rows
    - JOIN outputs
    - reports
    - NULL values
    - empty results
    """

    try:
        # -----------------------------------
        # CASE 0: No Result
        # -----------------------------------
        if not query_result:
            return "No matching data found."

        sql_lower = sql_query.lower()

        # -----------------------------------
        # CASE 1: Single Row + Single Column
        # Example:
        # [(20000,)]
        # [('John',)]
        # -----------------------------------
        if len(query_result) == 1 and len(query_result[0]) == 1:

            value = query_result[0][0]

            if value is None:
                return "No relevant data found."

            # -----------------------------------
            # Numeric Results
            # -----------------------------------
            if isinstance(value, (int, float)):

                # COUNT Query
                if "count(" in sql_lower:
                    return f"The total count is {value}."

                # AVG Query
                elif "avg(" in sql_lower:
                    return f"The average value is {value:,}."

                # SUM Query
                elif "sum(" in sql_lower:
                    return f"The total value is {value:,}."

                # Difference Calculation
                elif "max(" in sql_lower and "-" in sql_query:
                    return f"The calculated difference is ₹{value:,}."

                # Highest Value
                elif "max(" in sql_lower:
                    return f"The highest value is ₹{value:,}."

                # Lowest Value
                elif "min(" in sql_lower:
                    return f"The lowest value is ₹{value:,}."

                # Generic Numeric
                else:
                    return f"The result is {value:,}."

            # -----------------------------------
            # Text Result
            # -----------------------------------
            return f"The result is: {value}"

        # -----------------------------------
        # CASE 2: Multiple Rows + Single Column
        # Example:
        # [('Mary',), ('Alex',)]
        # -----------------------------------
        if all(len(row) == 1 for row in query_result):

            values = [
                str(row[0]) if row[0] is not None else "NULL"
                for row in query_result
            ]

            final_output = "\n".join(values)

            return (
                f"Here are the matching records:\n\n"
                f"{final_output}"
            )

        # -----------------------------------
        # CASE 3: Multiple Rows + Multiple Columns
        # Example:
        # [('John', 50000, 'IT')]
        # -----------------------------------
        formatted_rows = []

        for row in query_result:
            row_text = " | ".join(
                str(item) if item is not None else "NULL"
                for item in row
            )
            formatted_rows.append(row_text)

        final_output = "\n\n".join(formatted_rows)

        return (
            f"Here are the matching records:\n\n"
            f"{final_output}"
        )

    except Exception as e:
        return f"Response generation error: {str(e)}"