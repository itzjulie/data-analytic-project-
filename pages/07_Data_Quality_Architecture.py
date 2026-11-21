"""
BUILD-09 | pages/07_Data_Quality_Architecture.py
Live SQLite schema verification, row count checks, constraint audit and project info page.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
import pandas as pd
import sqlite3

from src.data.db import get_connection, DEFAULT_DB_PATH
from src.data.loader import load_analytical_data
from src.data.validator import validate_analytical_schema
from src.ui.components import render_tailwind_header
from src.ui.filters import render_sidebar_filters

st.set_page_config(page_title="Data Quality | Project P104", page_icon="🛡️", layout="wide")

df_full = load_analytical_data()
df = render_sidebar_filters(df_full)

render_tailwind_header(
    title="🛡️ Data Quality & Architecture",
    subtitle="Live SQLite Schema Verification · Row Counts · FK Constraints · Project Information",
    badge_text="DQ Audit"
)
st.markdown("---")

# ── Live schema verification ──────────────────────────────────────────────────
st.subheader("🗄️ Live Database Schema Verification")
st.caption(f"Connected to: `{DEFAULT_DB_PATH}`")

try:
    with get_connection(DEFAULT_DB_PATH, read_only=True) as conn:
        # List all tables and views
        tables_df = pd.read_sql_query(
            "SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY type, name",
            conn
        )

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown("**Objects in app.db**")
        st.dataframe(tables_df, use_container_width=True, hide_index=True)

    with col_b:
        # Row counts per table
        row_counts = {}
        with get_connection(DEFAULT_DB_PATH, read_only=True) as conn:
            for tbl in tables_df[tables_df["type"] == "table"]["name"].tolist():
                try:
                    cnt = pd.read_sql_query(f"SELECT COUNT(*) AS cnt FROM [{tbl}]", conn).iloc[0, 0]
                    row_counts[tbl] = cnt
                except Exception:
                    row_counts[tbl] = "Error"

        expected = {
            "dim_patients": 250,
            "dim_payers": 5,
            "fact_admissions": 300,
            "fact_clinical_diagnoses": 300,
            "fact_billing": 300,
        }

        rc_rows = []
        for tbl, cnt in row_counts.items():
            exp = expected.get(tbl)
            status = "✅ OK" if exp is None else ("✅ OK" if cnt == exp else f"⚠️ Expected {exp}")
            rc_rows.append({"Table": tbl, "Row Count": cnt, "Expected": exp or "—", "Status": status})

        rc_df = pd.DataFrame(rc_rows)
        st.markdown("**Row Count Verification**")
        st.dataframe(rc_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Database connection failed: {e}")

st.markdown("---")

# ── Schema inspection per table ───────────────────────────────────────────────
st.subheader("🔬 Per-Table Column Schema")

try:
    with get_connection(DEFAULT_DB_PATH, read_only=True) as conn:
        tbl_names = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", conn
        )["name"].tolist()

    for tbl in tbl_names:
        with get_connection(DEFAULT_DB_PATH, read_only=True) as conn:
            schema_df = pd.read_sql_query(f"PRAGMA table_info([{tbl}])", conn)
        with st.expander(f"📋 {tbl} ({len(schema_df)} columns)", expanded=False):
            schema_df = schema_df.rename(columns={
                "cid": "ID", "name": "Column", "type": "SQLite Type",
                "notnull": "NOT NULL", "dflt_value": "Default", "pk": "PK"
            })
            st.dataframe(schema_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Schema inspection error: {e}")

st.markdown("---")

# ── Data quality issues detected ──────────────────────────────────────────────
st.subheader("🧹 Data Quality Audit — Cleaned Cohort")

if len(df) > 0:
    n_total = len(df)
    
    missing_counts = df.isnull().sum()
    missing_nonzero = missing_counts[missing_counts > 0]
    
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        st.metric("Total Records Loaded", f"{n_total:,}")
    with col_q2:
        st.metric("Columns with Missing Data", f"{len(missing_nonzero)}")
    with col_q3:
        dup_count = df.duplicated(subset=["patient_id", "admission_id"]).sum() if "admission_id" in df.columns else 0
        st.metric("Duplicate Rows Detected", f"{dup_count}")

    if len(missing_nonzero) > 0:
        st.markdown("**Missing Value Summary (after cleaning)**")
        miss_df = pd.DataFrame({
            "Column": missing_nonzero.index,
            "Missing Count": missing_nonzero.values,
            "Missing %": (missing_nonzero.values / n_total * 100).round(2)
        })
        st.dataframe(miss_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No missing values in the analytical master view after cleaning.")

st.markdown("---")

# ── Project & Academic Information ───────────────────────────────────────────
st.subheader("🎓 Project Information")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown("""
| Field | Value |
|-------|-------|
| **Project** | Patient Demographic Analysis |
| **Project No.** | Project P104 |
| **Roll No.** | 2503201450068 |
| **Candidate** | Juli |
| **Programme** | MCA 2nd Year — Data Analytics |
| **Institution** | ABES Engineering College |
| **Mentor** | Mr. Dinesh |
| **Submission** | Academic Year 2024-25 |
""")

with col_info2:
    st.markdown("""
| Technical Item | Value |
|----------------|-------|
| **Language** | Python 3.12 |
| **Framework** | Streamlit Multipage |
| **CSS** | Tailwind CDN (iframe sandbox) |
| **Database** | SQLite 3 (`data/app.db`) |
| **Charts** | Plotly Express + Graph Objects |
| **Statistics** | SciPy + statsmodels |
| **Testing** | pytest + Streamlit AppTest |
| **Data** | Synthetic (seed=42, NCR India) |
| **Deployment** | Streamlit Community Cloud |
""")

st.markdown("---")

# ── OQ / BR Coverage ──────────────────────────────────────────────────────────
st.subheader("📋 Objectives & Requirements Coverage")
coverage = pd.DataFrame({
    "OQ ID": [f"OQ-{i:02d}" for i in range(1, 9)],
    "Research Question": [
        "Age-sex demographic distribution",
        "Chronic disease prevalence & co-occurrence",
        "Inpatient Length of Stay distribution",
        "Admission acuity (Emergency/Urgent/Elective)",
        "30-day hospital readmission rates",
        "Patient out-of-pocket financial burden",
        "Geographic catchment & service area",
        "Longitudinal admission trend analysis"
    ],
    "Dashboard Page": [
        "Demographics", "Comorbidities", "ALoS & Acuity",
        "ALoS & Acuity", "Readmission Risk",
        "Financial & Catchment", "Financial & Catchment", "Overview"
    ],
    "Statistical Method": [
        "Descriptive + Pyramid Chart", "Chi-Square + Correlation Matrix",
        "Kruskal-Wallis + Tukey IQR", "100% Stacked Bar (Proportional)",
        "Chi-Square Independence", "Box-Whisker + Mann-Whitney U",
        "Bubble Scatter (Spatial)", "Rolling SMA(30)"
    ]
})
st.dataframe(coverage, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("🎓 Project P104 | Roll No: 2503201450068 | ABES Engineering College | Mentor: Mr. Dinesh")
