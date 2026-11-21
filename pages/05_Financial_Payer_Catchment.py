"""
BUILD-08 | pages/05_Financial_Payer_Catchment.py
OQ-06 / OQ-07: Patient out-of-pocket liability by payer and geographic catchment density.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.data.loader import load_analytical_data
from src.analytics.statistics import compute_kpi_summary
from src.analytics.charts import plot_billing_violin, plot_catchment_map, NAVY, SKY_BLUE, EMERALD, AMBER
from src.ui.components import render_tailwind_header, render_kpi_card
from src.ui.filters import render_sidebar_filters

st.set_page_config(page_title="Financial & Catchment | Project P104", page_icon="💰", layout="wide")

df_full = load_analytical_data()
df = render_sidebar_filters(df_full)

render_tailwind_header(
    title="💰 Financial Burden & Geographic Catchment",
    subtitle="OQ-06 · OQ-07 · Out-of-Pocket Liability, Payer Reimbursement & Regional Patient Inflow",
    badge_text="Financial"
)
st.markdown("---")

kpi = compute_kpi_summary(df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("Total Charges", f"₹{kpi['total_charges']:,.0f}",
                    "Gross billing in cohort", "OQ-06", "blue")
with col2:
    render_kpi_card("Insurance Covered", f"₹{kpi['total_insurance_paid']:,.0f}",
                    f"Coverage ratio: {kpi['coverage_ratio']:.1%}", "OQ-06", "emerald")
with col3:
    render_kpi_card("Total Out-of-Pocket", f"₹{kpi['total_out_of_pocket']:,.0f}",
                    f"Median per encounter: ₹{kpi['median_out_of_pocket']:,.0f}", "OQ-06", "rose")
with col4:
    pct_urban = round((df["district_type"] == "Urban").mean() * 100, 1) if len(df) > 0 else 0
    unique_cities = df["city"].nunique() if len(df) > 0 else 0
    render_kpi_card("Catchment Cities", f"{unique_cities}",
                    f"{pct_urban}% urban origin", "OQ-07", "indigo")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("🎻 Out-of-Pocket Distribution by Payer")
    st.caption("OQ-06 · Box & whisker plot of patient financial liability stratified by insurance payer tier.")
    if len(df) == 0:
        st.info("No data for current filters.")
    else:
        st.plotly_chart(plot_billing_violin(df), use_container_width=True)

with col_b:
    st.subheader("🗺️ Geographic Catchment — Patient Inflow by City")
    st.caption("OQ-07 · Bubble size scales with admission volume per municipality; colour by urban/rural zone.")
    if len(df) == 0:
        st.info("No data for current filters.")
    else:
        st.plotly_chart(plot_catchment_map(df), use_container_width=True)

st.markdown("---")

# ── Payer Reimbursement Comparison Table ──────────────────────────────────────
st.subheader("🏦 Payer Reimbursement Comparison Table")
st.caption("OQ-06 · Average charges, insurance reimbursement and patient liability by payer. Sorted by coverage ratio.")

if len(df) > 0 and "payer_name" in df.columns:
    payer_summary = (
        df.groupby("payer_name", observed=False)
        .agg(
            Encounters=("patient_id", "count"),
            Avg_Total_Charges=("total_charges", "mean"),
            Avg_Insurance_Paid=("insurance_paid", "mean"),
            Avg_OOP=("out_of_pocket", "mean"),
            Coverage_Ratio=("insurance_paid", lambda x: (x.sum() / df.loc[x.index, "total_charges"].sum()))
        )
        .round(2)
        .reset_index()
        .sort_values("Coverage_Ratio", ascending=False)
    )
    payer_summary.columns = ["Payer", "Encounters", "Avg Total Charges (₹)",
                              "Avg Insurance Paid (₹)", "Avg OOP (₹)", "Coverage Ratio"]
    payer_summary["Coverage Ratio"] = payer_summary["Coverage Ratio"].apply(lambda x: f"{x:.1%}")
    st.dataframe(payer_summary, use_container_width=True, hide_index=True)
else:
    st.info("No payer data available.")

st.markdown("---")

# ── Regional Postal Zone Table ─────────────────────────────────────────────────
st.subheader("📍 Top Patient-Generating Postal Zones")
if len(df) > 0 and "zip_code" in df.columns:
    postal_df = (
        df.groupby(["zip_code", "city", "district_type"], observed=False)
        .agg(Admissions=("patient_id", "count"),
             Avg_OOP=("out_of_pocket", "mean"))
        .reset_index()
        .sort_values("Admissions", ascending=False)
        .head(15)
    )
    postal_df.columns = ["ZIP Code", "City", "District Type", "Admissions", "Avg OOP (₹)"]
    postal_df["Avg OOP (₹)"] = postal_df["Avg OOP (₹)"].round(0).astype(int)
    st.dataframe(postal_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("🎓 Project P104 | Roll No: 2503201450068 | ABES Engineering College | Mentor: Mr. Dinesh")
