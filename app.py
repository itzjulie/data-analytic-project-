"""
BUILD-06 | app.py — Main landing page (Overview / KPI Dashboard)
Patient Demographic Analysis · Project P104 · ABES MCA 2024-25
Roll No: 2503201450068 | Mentor: Mr. Dinesh
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

from src.data.loader import load_analytical_data
from src.analytics.statistics import compute_kpi_summary
from src.analytics.charts import plot_population_pyramid, plot_admission_timeline
from src.ui.components import render_tailwind_header, render_kpi_card, render_alert_box
from src.ui.filters import render_sidebar_filters

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Patient Demographic Analysis · Project P104",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Patient Demographic Analysis | ABES Engineering College | MCA 2nd Year",
    }
)

# ── Load Data ────────────────────────────────────────────────────────────────
df_full = load_analytical_data()

# ── Sidebar Filters ──────────────────────────────────────────────────────────
df = render_sidebar_filters(df_full)

# ── Tailwind Header ──────────────────────────────────────────────────────────
render_tailwind_header(
    title="🏥 Patient Demographic Analysis",
    subtitle="Overview Dashboard · Healthcare Cohort Intelligence · ABES Engineering College · MCA Capstone Project P104",
    badge_text="Overview"
)

st.markdown("---")

# ── KPI Cards Row ────────────────────────────────────────────────────────────
kpi = compute_kpi_summary(df)
n_empty = len(df) == 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card(
        title="Unique Patients",
        value=f"{kpi['unique_patients']:,}",
        subtext=f"Out of {df_full['patient_id'].nunique():,} total registered",
        badge="OQ-01",
        color="blue"
    )
with col2:
    render_kpi_card(
        title="Total Encounters",
        value=f"{kpi['total_encounters']:,}",
        subtext=f"{kpi['emergency_ratio_pct']}% Emergency admissions",
        badge="OQ-04",
        color="indigo"
    )
with col3:
    render_kpi_card(
        title="Median ALoS",
        value=f"{kpi['median_los']} days",
        subtext=f"IQR: {kpi['q25_los']}–{kpi['q75_los']} days",
        badge="OQ-03",
        color="amber"
    )
with col4:
    render_kpi_card(
        title="30-Day Readmission",
        value=f"{kpi['readmission_rate_pct']}%",
        subtext="HRRP threshold: 15.0%",
        badge="OQ-05",
        color="rose" if kpi['readmission_rate_pct'] >= 15.0 else "emerald"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Readmission Alert ────────────────────────────────────────────────────────
if kpi['readmission_rate_pct'] >= 15.0:
    render_alert_box(
        title="⚠️ Readmission Rate Exceeds HRRP Threshold",
        message=(f"Current 30-day readmission rate is {kpi['readmission_rate_pct']}%, "
                 f"surpassing the 15% CMS/HRRP penalty threshold. "
                 f"Refer to the Readmission Risk page for cohort-level breakdown."),
        alert_type="warning"
    )

st.markdown("---")

# ── Charts Row ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📊 Demographic Population Pyramid")
    st.caption("OQ-01 · Age and sex distribution of the filtered patient cohort (bidirectional axis).")
    if n_empty:
        st.info("No data matches the current filter selection.")
    else:
        st.plotly_chart(plot_population_pyramid(df), use_container_width=True)

with col_right:
    st.subheader("📈 Longitudinal Admission Trends")
    st.caption("OQ-08 · Monthly admission volume with 30-day SMA overlay (Jan 2023 – Dec 2024).")
    if n_empty:
        st.info("No data matches the current filter selection.")
    else:
        st.plotly_chart(plot_admission_timeline(df), use_container_width=True)

st.markdown("---")

# ── Cohort Breakdown Table ───────────────────────────────────────────────────
st.subheader("🗂️ Cohort Demographic Breakdown")
st.caption("Cross-tabulation of age bracket × gender × average length of stay (ALoS) and readmission rate.")

if not n_empty:
    cohort_table = (
        df.groupby(["age_bracket", "gender"], observed=False)
        .agg(
            Encounters=("patient_id", "count"),
            Avg_ALoS=("length_of_stay", "mean"),
            Readmission_Rate=("readmitted_30d", "mean"),
            Emergency_Pct=("admission_type", lambda x: (x == "Emergency").mean() * 100)
        )
        .round(2)
        .reset_index()
    )
    cohort_table.columns = ["Age Bracket", "Gender", "Encounters", "Avg ALoS (days)",
                             "Readmission Rate (%)", "Emergency Admits (%)"]
    cohort_table["Readmission Rate (%)"] = (cohort_table["Readmission Rate (%)"] * 100).round(2)
    st.dataframe(cohort_table, use_container_width=True, hide_index=True)
else:
    st.warning("No data matches your current filters. Try widening the age range or selecting more categories.")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "🎓 **Project P104 — Patient Demographic Analysis** | "
    "Roll No: 2503201450068 | ABES Engineering College | MCA 2nd Year | "
    "Mentor: Mr. Dinesh | Data: Synthetic (Seed=42, NCR India)"
)
