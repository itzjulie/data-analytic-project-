"""
BUILD-06 | pages/01_Demographics.py — Demographic Deep-Dive Page
OQ-01: Age-sex distribution and urban/rural catchment breakdown.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.data.loader import load_analytical_data
from src.analytics.statistics import compute_kpi_summary
from src.analytics.charts import (
    plot_population_pyramid, plot_catchment_map, NAVY, SKY_BLUE, EMERALD, AMBER
)
from src.ui.components import render_tailwind_header, render_kpi_card
from src.ui.filters import render_sidebar_filters

st.set_page_config(page_title="Demographics | Project 66", page_icon="👥", layout="wide")

df_full = load_analytical_data()
df = render_sidebar_filters(df_full)

render_tailwind_header(
    title="👥 Demographic Profiling",
    subtitle="OQ-01 · OQ-07 · Age-Sex Distribution, Catchment Zone & Marital Status Analysis",
    badge_text="Demographics"
)
st.markdown("---")

kpi = compute_kpi_summary(df)
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("Unique Patients", f"{kpi['unique_patients']:,}",
                    "In filtered cohort", "OQ-01", "blue")
with col2:
    pct_senior = round((df["age"] >= 65).mean() * 100, 1) if len(df) > 0 else 0
    render_kpi_card("Senior (65+) Share", f"{pct_senior}%",
                    "Age ≥ 65 inpatients", "OQ-01", "amber")
with col3:
    pct_urban = round((df["district_type"] == "Urban").mean() * 100, 1) if len(df) > 0 else 0
    render_kpi_card("Urban Origin", f"{pct_urban}%",
                    "Urban district patients", "OQ-07", "emerald")
with col4:
    gender_counts = df["gender"].value_counts() if len(df) > 0 else pd.Series(dtype=int)
    dominant = gender_counts.idxmax() if len(gender_counts) > 0 else "N/A"
    dominant_pct = round(gender_counts.max() / len(df) * 100, 1) if len(df) > 0 else 0
    render_kpi_card("Dominant Gender", f"{dominant}",
                    f"{dominant_pct}% of cohort", "OQ-01", "indigo")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("📊 Population Pyramid — Age & Sex")
    st.caption("Bidirectional bar chart; males plotted left, females right.")
    if len(df) == 0:
        st.info("No data for current filters.")
    else:
        st.plotly_chart(plot_population_pyramid(df), use_container_width=True)

with col_b:
    st.subheader("🗺️ Catchment Bubble Map — City & District")
    st.caption("OQ-07 · Bubble size proportional to patient volume per municipality.")
    if len(df) == 0:
        st.info("No data for current filters.")
    else:
        st.plotly_chart(plot_catchment_map(df), use_container_width=True)

st.markdown("---")

# Marital Status & Blood Group breakdown
col_c, col_d = st.columns([1, 1])

with col_c:
    st.subheader("💍 Marital Status Distribution")
    if len(df) > 0 and "marital_status" in df.columns:
        ms_df = df["marital_status"].value_counts().reset_index()
        ms_df.columns = ["Marital Status", "Count"]
        fig_ms = px.pie(ms_df, names="Marital Status", values="Count",
                        color_discrete_sequence=[NAVY, SKY_BLUE, EMERALD, AMBER],
                        hole=0.4,
                        title="<b>Marital Status Breakdown</b>")
        fig_ms.update_layout(height=360, paper_bgcolor="#FFFFFF",
                             margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_ms, use_container_width=True)
    else:
        st.info("Marital status data not available.")

with col_d:
    st.subheader("🩸 Blood Group Distribution")
    if len(df) > 0 and "blood_group" in df.columns:
        bg_df = df["blood_group"].value_counts().reset_index()
        bg_df.columns = ["Blood Group", "Count"]
        fig_bg = px.bar(bg_df, x="Blood Group", y="Count",
                        color="Blood Group",
                        color_discrete_sequence=[NAVY, SKY_BLUE, EMERALD, AMBER,
                                                 "#8B5CF6", "#EF4444", "#F59E0B", "#10B981"],
                        title="<b>Blood Group Frequency Distribution</b>",
                        labels={"Count": "Patient Count"})
        fig_bg.update_layout(height=360, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                             showlegend=False, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_bg, use_container_width=True)
    else:
        st.info("Blood group data not available.")

st.markdown("---")
st.caption("🎓 Project 66 | Roll No: 2503201450068 | ABES Engineering College | Mentor: Gunjan Agrawal")
