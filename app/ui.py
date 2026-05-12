import streamlit as st
from database.db_connection import engine
import pandas as pd
from agents.sql_agent import generate_sql
from services.query_executor import execute_query
from services.table_service import delete_table
from services.table_service import create_dynamic_table
from services.table_service import upload_csv_to_db
from agents.response_agent import generate_business_response
from services.table_service import (
    get_all_tables,
    preview_table_data,
    generate_basic_analytics,
    save_query_history
)



st.set_page_config(
    page_title="AI Database Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- STYLING --------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(135deg, #f5f9ff 0%, #ffffff 100%);
}

.hero {
    background: linear-gradient(135deg, #1E3A8A, #2563EB, #3B82F6);
    padding: 32px;
    border-radius: 24px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 12px 30px rgba(37,99,235,0.18);
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
}

.hero-sub {
    font-size: 18px;
    margin-top: 8px;
    opacity: 0.95;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 22px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 6px 16px rgba(0,0,0,0.05);
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 14px;
    color: #111827;
}

.feature-box {
    background: #F8FAFC;
    padding: 12px 14px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    margin-bottom: 10px;
}

.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    font-size: 16px;
    font-weight: 700;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("⚙️ Control Panel")

    page = st.radio(
        "Navigate",
        [
            "Dashboard",
            "Create Table",
            "Upload CSV",
            "View Tables",
            "AI Chat",
            "Query History",
            "Delete Table"
        ]
    )

st.sidebar.markdown("---")
st.sidebar.info("Dynamic Multi-Agent DB Platform")

# -------------------- HERO --------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">🚀 AI-Powered Database Assistant</div>
    <div class="hero-sub">
        Create tables • Upload data • Ask business questions • Get instant AI insights
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Tables</h4>
            <h2>Unlimited</h2>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <h4>⚡ Query Engine</h4>
            <h2>Real-Time</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <h4>🤖 AI Agents</h4>
            <h2>Multi-Agent</h2>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💬 Ask Your Database Anything</div>', unsafe_allow_html=True)

        question = st.text_input(
            "Business Question",
            placeholder="Example: Show top 5 customers by revenue"
        )

        if st.button("✨ Generate Insights"):
            if question:
                st.success(f"Question Received: {question}")
                st.info("AI agents are generating SQL, validating, executing, and preparing results.")
            else:
                st.warning("Please enter a business question.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔥 Features</div>', unsafe_allow_html=True)

        features = [
            "Dynamic Table Creation",
            "CSV / Excel Upload",
            "Natural Language to SQL",
            "Schema Discovery Agent",
            "Validation Agent",
            "Live Query Execution",
            "Response Agent",
            "Docker + Cloud Ready"
        ]

        for f in features:
            st.markdown(f'<div class="feature-box">✅ {f}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- CREATE TABLE --------------------
elif page == "Create Table":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🛠 Create New Table</div>', unsafe_allow_html=True)

    table_name = st.text_input("Table Name", placeholder="Example: customers")
    columns = st.text_area(
        "Columns (comma separated)",
        placeholder="Example: customer_name, revenue, city"
    )

    if st.button("Create Table"):
        if table_name and columns:
            st.success(f"Table '{table_name}' ready to be created")
        else:
            st.warning("Please provide table name and columns")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- CSV UPLOAD --------------------
elif page == "Upload CSV":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📂 Upload CSV File</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

    table_name = st.text_input(
        "Table Name for CSV Data",
        placeholder="Example: customers"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

    if st.button("Upload CSV to Database"):
        if table_name:
            result = upload_csv_to_db(
                uploaded_file,
                table_name
            )
            st.success(result)
        else:
            st.warning("Please provide a table name")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- AI CHAT --------------------
elif page == "AI Chat":

    st.markdown("## AI Chat Assistant")

    chat_question = st.text_input(
        "Ask your business question",
        placeholder="Example: Which employee has highest salary?"
    )

    if st.button("Ask AI"):

        if chat_question:

            generated_sql = generate_sql(
                chat_question
            )

            raw_result = execute_query(
                generated_sql
            )

            final_result = generate_business_response(
                chat_question,
                raw_result
            )

            save_query_history(
                chat_question,
                generated_sql,
                final_result
            )

            st.success("Query processed successfully")

            st.markdown("### Generated SQL")
            st.code(generated_sql)

            st.markdown("### Final Result")
            st.info(final_result)
        else:
            st.warning("Please enter a question")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- QUERY HISTORY --------------------
elif page == "Query History":

    st.markdown("## Query History")

    try:
        history_df = pd.read_sql(
            "SELECT * FROM query_history ORDER BY id DESC",
            engine
        )

        if not history_df.empty:
            st.dataframe(
                history_df,
                use_container_width=True
            )
        else:
            st.warning("No query history found")

    except Exception:
        st.warning("No query history available yet")    
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- DELETE TABLE --------------------
elif page == "Delete Table":

    st.markdown("## Delete Existing Table")

    tables = get_all_tables()

    if tables:
        selected_table = st.selectbox(
            "Select Table to Delete",
            tables
        )

        st.warning(
            f"Warning: This will permanently delete '{selected_table}'"
        )

        if st.button("Delete Selected Table"):
            result = delete_table(selected_table)
            st.success(result)

    else:
        st.warning(
            "No tables available to delete"
        )

elif page == "View Tables":

    st.markdown("## View Existing Tables")

    tables = get_all_tables()

    if tables:
        selected_table = st.selectbox(
            "Select Table",
            tables
        )

        if selected_table:
            st.success(
                f"Selected Table: {selected_table}"
            )

            preview_df = preview_table_data(
                selected_table
            )

            if not preview_df.empty:
                st.markdown("### Table Preview")

                st.dataframe(
                    preview_df,
                    use_container_width=True
                )

                st.markdown("### Auto Analytics Dashboard")

                analytics_df = generate_basic_analytics(
                    selected_table
                )

                numeric_cols = analytics_df.select_dtypes(
                    include=["int64", "float64"]
                ).columns

                if len(numeric_cols) > 0:
                    selected_numeric = st.selectbox(
                        "Select Numeric Column for Chart",
                        numeric_cols
                    )

                    st.bar_chart(
                        analytics_df[selected_numeric]
                    )

                else:
                    st.warning(
                        "No numeric columns found for analytics"
                    )

            else:
                st.warning(
                    "No data found in this table"
                )

    else:
        st.warning(
            "No tables found in database"
        )
# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("Built with Streamlit + SQLite + OpenRouter + FastAPI + Docker + Multi-Agent Architecture")
