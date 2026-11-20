"""
BUILD-09 | pages/06_Data_Explorer.py
Multi-column search, interactive dataframe viewer, CSV download for filtered cohort.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
import pandas as pd
import io

from src.data.loader import load_analytical_data
from src.ui.components import render_tailwind_header
from src.ui.filters import render_sidebar_filters

st.set_page_config(page_title="Data Explorer | Project 66", page_icon="🔎", layout="wide")

df_full = load_analytical_data()
df = render_sidebar_filters(df_full)

render_tailwind_header(
    title="🔎 Data Explorer",
    subtitle="Interactive cohort viewer — search, sort, filter columns and export to CSV",
    badge_text="Explorer"
)
st.markdown("---")

st.markdown(f"**Filtered Cohort:** {len(df):,} of {len(df_full):,} encounters | {df.shape[1]} columns")

# ── Column selector ───────────────────────────────────────────────────────────
all_cols = df.columns.tolist()
default_cols = [
    "patient_id", "full_name", "age", "gender", "age_bracket",
    "city", "department", "admission_type", "length_of_stay",
    "primary_diagnosis", "readmitted_30d", "payer_name",
    "total_charges", "out_of_pocket"
]
default_cols = [c for c in default_cols if c in all_cols]

selected_cols = st.multiselect(
    "📋 Select Columns to Display",
    options=all_cols,
    default=default_cols,
    help="Choose which columns to include in the table view."
)
if not selected_cols:
    selected_cols = default_cols

# ── Free-text search ──────────────────────────────────────────────────────────
search_term = st.text_input(
    "🔍 Search (matches any text column — name, diagnosis, city, ZIP…)",
    placeholder="e.g. Priya, Noida, Hypertension, 201301",
    help="Case-insensitive substring search across all string columns."
)

# Apply free-text search across string columns
if search_term.strip():
    str_cols = df[selected_cols].select_dtypes(include="object").columns
    if len(str_cols) > 0:
        mask = df[str_cols].apply(
            lambda col: col.astype(str).str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        df_view = df[mask][selected_cols]
    else:
        df_view = df[selected_cols]
else:
    df_view = df[selected_cols]

st.caption(f"Showing {len(df_view):,} records matching current filters and search.")

# ── Dataframe viewer ──────────────────────────────────────────────────────────
st.dataframe(
    df_view.reset_index(drop=True),
    use_container_width=True,
    height=500
)

st.markdown("---")

# ── Export buttons ────────────────────────────────────────────────────────────
col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    csv_bytes = df_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Cohort as CSV",
        data=csv_bytes,
        file_name="patient_cohort_filtered.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary"
    )

with col_dl2:
    # Full analytical master (all columns, filtered rows)
    full_csv = df[all_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download All Columns (Full Schema)",
        data=full_csv,
        file_name="patient_cohort_full_schema.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")

# ── Descriptive statistics ────────────────────────────────────────────────────
st.subheader("📐 Descriptive Statistics — Numeric Columns")
num_df = df_view.select_dtypes(include="number")
if not num_df.empty:
    st.dataframe(num_df.describe().round(3), use_container_width=True)
else:
    st.info("No numeric columns in current column selection.")

st.markdown("---")
st.caption("🎓 Project 66 | Roll No: 2503201450068 | ABES Engineering College | Mentor: Gunjan Agrawal")
