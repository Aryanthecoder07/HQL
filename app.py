# app.py
import streamlit as st
import os
from core.db_utils import get_connection, list_tables, fetch_table
from core.gemini_llm import get_sql_from_hql

# Sidebar: Ask user for custom DB name
st.sidebar.title("🗂 Database Explorer")
user_db_name = st.sidebar.text_input("Enter database filename (without .sqlite)", value="hql_db")
DB_PATH = f"database/{user_db_name}.sqlite"

# Ensure database directory exists
os.makedirs("database", exist_ok=True)

# Connect to SQLite DB
conn = get_connection(DB_PATH)
cursor = conn.cursor()

# List tables in sidebar
tables = list_tables(cursor)
selected_table = st.sidebar.selectbox("Select a table", tables if tables else ["No tables"])

# File uploader (load custom DB file)
uploaded_file = st.sidebar.file_uploader("📂 Load Saved DB", type=["sqlite", "db"])
if uploaded_file:
    with open(DB_PATH, "wb") as f:
        f.write(uploaded_file.read())
    st.sidebar.success(f"✅ Database '{user_db_name}.sqlite' loaded. Reload app to view updates.")

# File downloader (save current DB)
if os.path.exists(DB_PATH):
    with open(DB_PATH, "rb") as f:
        st.sidebar.download_button(
            f"💾 Save '{user_db_name}.sqlite'",
            data=f,
            file_name=f"{user_db_name}.sqlite"
        )

# Main area
st.title("🧠 HQL DBMS - Human Query Language")

user_input = st.text_area("💬 Enter your question in natural language")
if st.button("Run Query"):
    if user_input.strip():
        sql_query = get_sql_from_hql(user_input)
        st.code(sql_query, language="sql")

        try:
            cursor.execute(sql_query)

            if sql_query.strip().lower().startswith("select"):
                rows, columns = fetch_table(cursor, sql_query)
                st.table([columns] + rows)  # ✅ Using st.table without pandas
            else:
                conn.commit()
                st.success("✅ Query executed successfully.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# If user selects a table from sidebar
if selected_table and selected_table != "No tables":
    st.subheader(f"📊 Contents of `{selected_table}`")
    try:
        cursor.execute(f"SELECT * FROM {selected_table}")
        rows, columns = fetch_table(cursor, f"SELECT * FROM {selected_table}")
        st.table([columns] + rows)  # ✅ Again using st.table
    except Exception as e:
        st.error(f"❌ Cannot load table: {e}")
