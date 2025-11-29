# core/gemini_llm.py
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os


def get_sql_from_hql(hql_query: str) -> str:
    """Converts human query to SQL using Gemini Pro."""
    
    # Connect Gemini
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key = os.getenv("GOOGLE_API_KEY")
    )

    # Prompt Template
    prompt = PromptTemplate(
        input_variables=["human_query"],
        template="""
You are a helpful assistant that converts human requests into SQL queries for a SQLite database.
Only return the SQL query. Do not add explanation or formatting.

Human Query: {human_query}
SQL Query:
"""
    )

    # Combine and invoke
    chain = prompt | model
    response = chain.invoke({"human_query": hql_query})
    return response.content.strip()
