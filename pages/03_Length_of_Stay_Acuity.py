"""
BUILD-07 | pages/03_Length_of_Stay_Acuity.py
OQ-03 / OQ-04: ALoS box plots with Tukey fences and 100% stacked acuity bars.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
import pandas as pd

from src.data.loader import load_analytical_data
from src.analytics.statistics import compute_kpi_summary, detect_los_outliers
from src.analytics.charts import plot_los_box, plot_acuity_stacked_bar
from src.ui.components import render_tailwind_header, render_kpi_card, render_alert_box
from src.ui.filters import render_sidebar_filters

st.set_page_config(page_title="ALoS & Acuity | Project 66", page_icon="🛏️", layout="wide")

df_full = load_analytical_data()
df = render_sidebar_filters(df_full)

render_tailwind_header(
    title="🛏️ Length of Stay & Admission Acuity",
    subtitle="OQ-03 · OQ-04 · Inpatient Stay Distribution, Prolonged Stays & Acuity Triage Breakdown",
    badge_text="ALoS / Acuity"
)
st.markdown("---")

kpi = compute_kpi_summary(df)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("Median ALoS", f"{kpi['median_los']} days",
                    f"Mean: {kpi['mean_los']} days", "OQ-03", "blue")
with col2:
    render_kpi_card("IQR (ALoS)", f"{kpi['iqr_los']} days",
                    f"Q1={kpi['q25_los']} · Q3={kpi['q75_los']}", "OQ-03", "indigo")
with col3:
    prolonged_n = int((df["length_of_stay"] > 14).sum()) if len(df) > 0 else 0
    prolonged_pct = round(prolonged_n / len(df) * 100, 1) if len(df) > 0 else 0
    render_kpi_card("Prolonged Stays >14d", f"{prolonged_n}",
                    f"{prolonged_pct}% of cohort", "OQ-03",
                    "rose" if prolonged_pct > 10 else "amber")
with col4:
    render_kpi_card("Emergency Admits",
                    f"{kpi['emergency_ratio_pct']}%",
                    "of all admissions", "OQ-04",
                    "rose" if kpi["emergency_ratio_pct"] > 40 else "amber")

st.markdown("<br>", unsafe_allow_html=True)

if prolonged_pct > 10:
    render_alert_box(
        title="Prolonged Stay Volume Elevated",
        message=f"{prolonged_n} patients ({prolonged_pct}%) exceeded 14-day threshold. "
                "Review discharge planning protocols for geriatric and high-acuity cohorts.",
        alert_type="warning"
    )

st.markdown("---")

# ── Charts ─────────────────────────────────────────────────────────────────────
col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("📦 ALoS Box Plot — Age Bracket Distribution")
    st.caption("OQ-03 · Tukey IQR fences; outliers (>14 days) marked individually per age group.")
    if len(df) == 0:
        st.info("No data for current filters.")
    else:
        st.plotly_chart(plot_los_box(df), use_container_width=True)

with col_b:
    st.subheader("📊 Admission Acuity — 100% Stacked Bar")
    st.caption("OQ-04 · Proportional breakdown of Emergency / Urgent / Elective per age bracket.")
    if len(df) == 0:
        st.info("No data for current filters.")
    else:
        st.plotly_chart(plot_acuity_stacked_bar(df), use_container_width=True)

st.markdown("---")

# ── Prolonged Stays Table ─────────────────────────────────────────────────────
st.subheader("🚨 Prolonged Stay Patient Register (>14 Days)")
st.caption("All inpatients with LOS exceeding 14 days — sorted by descending LOS for clinical triage prioritisation.")

if len(df) > 0:
    df_outliers = detect_los_outliers(df)
    prolonged_df = df_outliers[df_outliers["length_of_stay"] > 14].copy()
    
    if len(prolonged_df) > 0:
        display_cols = [
            "patient_id", "full_name", "age", "gender", "age_bracket",
            "department", "admission_type", "length_of_stay",
            "primary_diagnosis", "is_statistical_outlier",
            "readmitted_30d", "payer_name"
        ]
        display_cols = [c for c in display_cols if c in prolonged_df.columns]
        
        col_rename = {
            "patient_id": "Patient ID", "full_name": "Name", "age": "Age",
            "gender": "Gender", "age_bracket": "Age Bracket",
            "department": "Department", "admission_type": "Acuity",
            "length_of_stay": "LOS (days)", "primary_diagnosis": "Primary Diagnosis",
            "is_statistical_outlier": "Tukey Outlier",
            "readmitted_30d": "30d Readmit", "payer_name": "Payer"
        }
        
        prolonged_df = (prolonged_df[display_cols]
                        .rename(columns=col_rename)
                        .sort_values("LOS (days)", ascending=False)
                        .reset_index(drop=True))
        st.dataframe(prolonged_df, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(prolonged_df)} prolonged-stay records.")
    else:
        st.success("✅ No patients with LOS >14 days in the current cohort.")
else:
    st.warning("No data matches the current filter selection.")

st.markdown("---")

# ── Department-wise ALoS table ─────────────────────────────────────────────────
st.subheader("🏥 Department-wise ALoS Summary")
if len(df) > 0 and "department" in df.columns:
    dept_los = (
        df.groupby("department", observed=False)["length_of_stay"]
        .agg(Count="count", Mean_ALoS="mean", Median_ALoS="median",
             Q75_ALoS=lambda x: x.quantile(0.75), Max_LOS="max")
        .round(2)
        .sort_values("Median_ALoS", ascending=False)
        .reset_index()
    )
    dept_los.columns = ["Department", "Encounters", "Mean ALoS", "Median ALoS", "Q75 ALoS", "Max LOS"]
    st.dataframe(dept_los, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("🎓 Project 66 | Roll No: 2503201450068 | ABES Engineering College | Mentor: Gunjan Agrawal")
