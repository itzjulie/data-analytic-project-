"""
BUILD-08 | pages/04_Readmission_Risk.py
OQ-05: 30-day readmission rate by demographic cohort with HRRP threshold alerts.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.data.loader import load_analytical_data
from src.analytics.statistics import compute_kpi_summary, compute_chi_square_independence
from src.analytics.charts import plot_readmission_bars, NAVY, SKY_BLUE, ROSE, AMBER, EMERALD
from src.ui.components import render_tailwind_header, render_kpi_card, render_alert_box
from src.ui.filters import render_sidebar_filters

st.set_page_config(page_title="Readmission Risk | Project 66", page_icon="🔄", layout="wide")

df_full = load_analytical_data()
df = render_sidebar_filters(df_full)

render_tailwind_header(
    title="🔄 Readmission Risk Analysis",
    subtitle="OQ-05 · 30-Day Readmission Rates by Demographic Cohort with HRRP Penalty Thresholds",
    badge_text="Readmission"
)
st.markdown("---")

kpi = compute_kpi_summary(df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("Overall Readmission Rate", f"{kpi['readmission_rate_pct']}%",
                    "HRRP threshold: 15.0%", "OQ-05",
                    "rose" if kpi["readmission_rate_pct"] >= 15 else "emerald")
with col2:
    n_readmit = int(df["readmitted_30d"].sum()) if len(df) > 0 else 0
    render_kpi_card("Readmitted Encounters", f"{n_readmit:,}",
                    f"of {len(df):,} total encounters", "OQ-05", "rose")
with col3:
    # Highest risk age bracket
    if len(df) > 0:
        worst = (df.groupby("age_bracket", observed=False)["readmitted_30d"]
                 .mean()
                 .idxmax())
        worst_rate = round(df.groupby("age_bracket", observed=False)["readmitted_30d"]
                           .mean()[worst] * 100, 1)
    else:
        worst, worst_rate = "N/A", 0.0
    render_kpi_card("Highest-Risk Bracket", f"{worst}",
                    f"Readmission rate: {worst_rate}%", "OQ-05", "amber")
with col4:
    # % of payers above threshold
    if len(df) > 0:
        payer_rates = (df.groupby("payer_name", observed=False)["readmitted_30d"].mean() * 100)
        payers_above = int((payer_rates >= 15).sum())
    else:
        payers_above = 0
    render_kpi_card("Payers Above Threshold", f"{payers_above}",
                    "payers with rate ≥15%", "OQ-05",
                    "rose" if payers_above > 0 else "emerald")

st.markdown("<br>", unsafe_allow_html=True)

if kpi["readmission_rate_pct"] >= 15.0:
    render_alert_box(
        title="⚠️ HRRP Penalty Threshold Exceeded — Clinical Intervention Required",
        message=(f"Overall 30-day readmission rate is {kpi['readmission_rate_pct']}%, "
                 f"exceeding the 15% CMS Hospital Readmissions Reduction Program (HRRP) threshold. "
                 f"The highest-risk bracket is '{worst}' at {worst_rate}%. "
                 "Implement discharge medication reconciliation and 72-hour follow-up protocols."),
        alert_type="warning"
    )

st.markdown("---")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("📊 Readmission Rate — Age Bracket Bar Chart")
    st.caption("Bars coloured crimson when cohort rate ≥ 15% (HRRP penalty band). Dashed reference line marks threshold.")
    if len(df) == 0:
        st.info("No data for current filters.")
    else:
        st.plotly_chart(plot_readmission_bars(df), use_container_width=True)

with col_b:
    st.subheader("🏥 Readmission Rate by Department")
    st.caption("Which clinical specialties contribute disproportionately to 30-day returns.")
    if len(df) > 0 and "department" in df.columns:
        dept_df = (df.groupby("department", observed=False)["readmitted_30d"]
                   .agg(["mean", "count"])
                   .reset_index())
        dept_df["rate_pct"] = (dept_df["mean"] * 100).round(1)
        dept_df = dept_df.sort_values("rate_pct", ascending=True)
        colors = [ROSE if r >= 15 else SKY_BLUE for r in dept_df["rate_pct"]]
        import plotly.graph_objects as go
        fig_dept = go.Figure(go.Bar(
            y=dept_df["department"], x=dept_df["rate_pct"],
            orientation="h",
            marker=dict(color=colors),
            text=[f"{r}%" for r in dept_df["rate_pct"]],
            textposition="auto"
        ))
        fig_dept.add_vline(x=15, line_dash="dash", line_color=ROSE,
                           annotation_text="15% Threshold")
        fig_dept.update_layout(
            title="<b>Readmission Rate (%) by Department</b>",
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            xaxis=dict(title="Rate (%)", gridcolor="#E2E8F0"),
            height=380, margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_dept, use_container_width=True)
    else:
        st.info("No data available.")

st.markdown("---")

# ── Comorbidity Risk Breakdown ─────────────────────────────────────────────────
st.subheader("🫀 Readmission Rate by Comorbidity Burden")
st.caption("Patients with ≥2 chronic conditions (multimorbid) tend to have higher readmission rates.")

if len(df) > 0 and "is_multimorbid" in df.columns:
    mm_rate = (df.groupby("is_multimorbid", observed=False)["readmitted_30d"]
               .agg(Rate="mean", Count="count")
               .reset_index())
    mm_rate["Rate (%)"] = (mm_rate["Rate"] * 100).round(2)
    mm_rate["Multimorbid"] = mm_rate["is_multimorbid"].map({True: "Yes (≥2 conditions)", False: "No"})
    mm_rate = mm_rate[["Multimorbid", "Count", "Rate (%)"]].rename(columns={"Count": "Encounters"})
    st.dataframe(mm_rate, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Chi-Square test ───────────────────────────────────────────────────────────
st.subheader("📐 Statistical Test: Age Bracket → Readmission Independence")
if len(df) > 10:
    try:
        chi = compute_chi_square_independence(df, "age_bracket", "readmitted_30d")
        c1, c2, c3 = st.columns(3)
        c1.metric("χ² Statistic", chi["chi2_stat"])
        c2.metric("p-value", chi["p_value"])
        c3.metric("Degrees of Freedom", chi["dof"])
        if chi["is_significant"]:
            st.success("✅ Significant association (p < 0.05): age bracket meaningfully predicts 30-day readmission.")
        else:
            st.info("ℹ️ No significant association detected at α = 0.05.")
    except Exception as e:
        st.warning(f"Test could not complete: {e}")

st.markdown("---")
st.caption("🎓 Project 66 | Roll No: 2503201450068 | ABES Engineering College | Mentor: Gunjan Agrawal")
