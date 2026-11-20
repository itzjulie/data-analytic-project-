import contextlib
import streamlit as st
import pandas as pd
from src.data.db import get_connection, DEFAULT_DB_PATH
from src.data.validator import validate_analytical_schema
from src.data.cleaner import clean_and_enrich_data


@st.cache_data(ttl=3600, show_spinner=False)
def load_analytical_data(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """
    Loads and caches the complete analytical master dataset from SQLite.
    Uses contextlib.closing() to ensure the connection is properly closed
    after the query — required because sqlite3.Connection.__exit__ only
    commits/rolls back; it does NOT close the connection.
    Cached for 3600 s to guarantee sub-150 ms UI response times.
    """
    with contextlib.closing(get_connection(db_path, read_only=True)) as conn:
        df = pd.read_sql_query("SELECT * FROM v_patient_analytical_master", conn)

    df = validate_analytical_schema(df)
    df = clean_and_enrich_data(df)
    return df
