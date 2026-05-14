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


def generate_human_response(
    question,
    sql_query,
    query_result
):
    """
    Convert SQL result into safe business response
    without hallucination
    """

    try:
        # Handle empty result
        if not query_result:
            return "No matching data found."

        # Extract first value safely
        first_value = query_result[0][0]

        if first_value is None:
            return "No relevant data found."

        # Numeric result formatting
        if isinstance(first_value, (int, float)):

            if "salary" in question.lower():
                return (
                    f"The result for your query is ₹{first_value:,}."
                )

            elif "count" in question.lower() or "how many" in question.lower():
                return (
                    f"The total count is {first_value}."
                )

            elif "sum" in question.lower() or "total" in question.lower():
                return (
                    f"The total value is {first_value:,}."
                )

            else:
                return (
                    f"The result is {first_value:,}."
                )

        # Text result formatting
        return f"The result is: {first_value}"

    except Exception as e:
        return f"Response generation error: {str(e)}"