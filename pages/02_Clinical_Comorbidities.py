"""
BUILD-07 | pages/02_Clinical_Comorbidities.py
OQ-02: Disease prevalence, chronic condition co-occurrence & Chi-Square independence test.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.data.loader import load_analytical_data
from src.analytics.statistics import compute_comorbidity_matrix, compute_chi_square_independence
from src.analytics.charts import plot_comorbidity_heatmap, NAVY, SKY_BLUE, ROSE, EMERALD, AMBER
from src.ui.components import render_tailwind_header, render_kpi_card, render_alert_box
from src.ui.filters import render_sidebar_filters

st.set_page_config(page_title="Comorbidities | Project 66", page_icon="🫀", layout="wide")

df_full = load_analytical_data()
df = render_sidebar_filters(df_full)

render_tailwind_header(
    title="🫀 Clinical Comorbidity Analysis",
    subtitle="OQ-02 · Chronic Condition Prevalence, Co-occurrence Patterns & Statistical Independence Testing",
    badge_text="Comorbidities"
)
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
conditions = {
    "hypertension": "Hypertension",
    "diabetes":     "Diabetes T2",
    "cvd":          "CVD",
    "copd":         "COPD",
    "ckd":          "CKD"
}

cols = st.columns(5)
for i, (col_name, label) in enumerate(conditions.items()):
    if col_name in df.columns and len(df) > 0:
        pct = round(df[col_name].mean() * 100, 1)
    else:
        pct = 0.0
    color = "rose" if pct > 50 else "amber" if pct > 30 else "blue"
    with cols[i]:
        render_kpi_card(label, f"{pct}%", f"of {len(df):,} encounters", "OQ-02", color)

st.markdown("<br>", unsafe_allow_html=True)

# Multimorbidity KPI
if "is_multimorbid" in df.columns and len(df) > 0:
    mm_pct = round(df["is_multimorbid"].mean() * 100, 1)
    render_alert_box(
        title="Multimorbidity Burden",
        message=f"{mm_pct}% of the filtered cohort carry ≥2 chronic conditions simultaneously. "
                "This elevates readmission risk and complicates discharge planning.",
        alert_type="warning" if mm_pct > 40 else "info"
    )

st.markdown("---")

# ── Charts ─────────────────────────────────────────────────────────────────────
col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("🔥 Comorbidity Co-occurrence Heatmap")
    st.caption("Pairwise Pearson correlation across 5 chronic conditions (1 = always co-present).")
    if len(df) > 1:
        corr_df = compute_comorbidity_matrix(df)
        st.plotly_chart(plot_comorbidity_heatmap(corr_df), use_container_width=True)
    else:
        st.info("Insufficient data to compute correlations.")

with col_b:
    st.subheader("📊 Disease Prevalence Bar Chart")
    st.caption("Absolute count and relative share of each chronic condition in the cohort.")
    if len(df) > 0:
        prev_data = {label: int(df[col].sum()) for col, label in conditions.items() if col in df.columns}
        prev_df = pd.DataFrame(list(prev_data.items()), columns=["Condition", "Count"])
        prev_df["Prevalence (%)"] = (prev_df["Count"] / len(df) * 100).round(1)
        fig_prev = px.bar(
            prev_df, x="Condition", y="Count", color="Condition",
            text="Prevalence (%)",
            color_discrete_sequence=[ROSE, AMBER, NAVY, SKY_BLUE, EMERALD],
            title="<b>Chronic Condition Prevalence in Filtered Cohort</b>",
            labels={"Count": "Patient Count"}
        )
        fig_prev.update_traces(texttemplate="%{text}%", textposition="outside")
        fig_prev.update_layout(showlegend=False, plot_bgcolor="#FFFFFF",
                               paper_bgcolor="#FFFFFF", height=380,
                               margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_prev, use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Cross-tabulation matrix ───────────────────────────────────────────────────
st.subheader("📋 Condition × Condition Cross-tabulation Matrix")
st.caption("Count of encounters where both conditions are simultaneously present.")
if len(df) > 0 and all(c in df.columns for c in conditions):
    cond_cols = list(conditions.keys())
    cond_labels = list(conditions.values())
    sub = df[cond_cols].copy().astype(int)
    crosstab_data = {}
    for c1, l1 in zip(cond_cols, cond_labels):
        crosstab_data[l1] = {}
        for c2, l2 in zip(cond_cols, cond_labels):
            crosstab_data[l1][l2] = int((sub[c1] & sub[c2]).sum())
    crosstab_df = pd.DataFrame(crosstab_data)
    st.dataframe(crosstab_df, use_container_width=True)
else:
    st.info("No data available.")

st.markdown("---")

# ── Chi-Square test ───────────────────────────────────────────────────────────
st.subheader("📐 Chi-Square Test of Independence")
st.caption("OQ-02 · Tests whether age bracket or gender significantly predicts presence of comorbidity.")

if len(df) > 10:
    chi_col1, chi_col2 = st.columns(2)
    
    with chi_col1:
        st.markdown("**Age Bracket → Hypertension**")
        try:
            result = compute_chi_square_independence(df, "age_bracket", "hypertension")
            st.metric("χ² Statistic", result["chi2_stat"])
            st.metric("p-value", result["p_value"])
            st.metric("Degrees of Freedom", result["dof"])
            if result["is_significant"]:
                st.success("✅ Statistically significant (p < 0.05) — age bracket predicts hypertension.")
            else:
                st.info("ℹ️ Not significant at α = 0.05 level.")
        except Exception as e:
            st.warning(f"Chi-Square test could not run: {e}")

    with chi_col2:
        st.markdown("**Gender → Diabetes T2**")
        try:
            result2 = compute_chi_square_independence(df, "gender", "diabetes")
            st.metric("χ² Statistic", result2["chi2_stat"])
            st.metric("p-value", result2["p_value"])
            st.metric("Degrees of Freedom", result2["dof"])
            if result2["is_significant"]:
                st.success("✅ Statistically significant (p < 0.05) — gender predicts diabetes.")
            else:
                st.info("ℹ️ Not significant at α = 0.05 level.")
        except Exception as e:
            st.warning(f"Chi-Square test could not run: {e}")
else:
    st.warning("Insufficient cohort size for statistical testing. Broaden the filters.")

st.markdown("---")
st.caption("🎓 Project 66 | Roll No: 2503201450068 | ABES Engineering College | Mentor: Gunjan Agrawal")
