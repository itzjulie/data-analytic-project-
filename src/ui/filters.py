"""
BUILD-05: Sidebar filter renderer with st.session_state persistence.
Applies globally across all Streamlit pages via shared session state.
"""
import streamlit as st
import pandas as pd


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders interactive sidebar filters and returns filtered DataFrame.
    All filter state is persisted in st.session_state for cross-page sharing.

    Filters applied:
        - age_range   : slider (min_age .. max_age)
        - selected_genders   : multiselect (Male / Female / Other)
        - selected_payers    : multiselect (payer names)
        - selected_departments : multiselect (department names)

    Returns:
        pd.DataFrame: Filtered copy of the analytical master view.
    """
    with st.sidebar:
        st.markdown("## 🔍 Global Cohort Filters")
        st.caption("Filters apply across **all** dashboard pages.")
        st.divider()

        # ── Age Range ────────────────────────────────────────────────────────
        min_age = int(df["age"].min()) if not df.empty else 0
        max_age = int(df["age"].max()) if not df.empty else 100

        default_age = st.session_state.get("age_range", (min_age, max_age))
        # Clamp defaults to current data range
        default_age = (max(min_age, default_age[0]), min(max_age, default_age[1]))

        age_range = st.slider(
            "Patient Age Range",
            min_value=min_age,
            max_value=max_age,
            value=default_age,
            step=1,
            help="Slide to restrict the analysis to a specific age cohort."
        )
        st.session_state["age_range"] = age_range

        st.divider()

        # ── Gender ───────────────────────────────────────────────────────────
        gender_options = sorted(df["gender"].dropna().unique().tolist())
        default_genders = st.session_state.get("selected_genders", gender_options)
        default_genders = [g for g in default_genders if g in gender_options] or gender_options

        selected_genders = st.multiselect(
            "Gender",
            options=gender_options,
            default=default_genders,
            help="Select one or more genders to include in the cohort."
        )
        if not selected_genders:
            selected_genders = gender_options  # Prevent empty selection lock-out
        st.session_state["selected_genders"] = selected_genders

        st.divider()

        # ── Insurance Payer ──────────────────────────────────────────────────
        payer_options = sorted(df["payer_name"].dropna().unique().tolist())
        default_payers = st.session_state.get("selected_payers", payer_options)
        default_payers = [p for p in default_payers if p in payer_options] or payer_options

        selected_payers = st.multiselect(
            "Insurance Payer",
            options=payer_options,
            default=default_payers,
            help="Filter patients by their primary insurance provider."
        )
        if not selected_payers:
            selected_payers = payer_options
        st.session_state["selected_payers"] = selected_payers

        st.divider()

        # ── Department ───────────────────────────────────────────────────────
        dept_options = sorted(df["department"].dropna().unique().tolist())
        default_depts = st.session_state.get("selected_departments", dept_options)
        default_depts = [d for d in default_depts if d in dept_options] or dept_options

        selected_departments = st.multiselect(
            "Clinical Department",
            options=dept_options,
            default=default_depts,
            help="Restrict analysis to specific inpatient departments."
        )
        if not selected_departments:
            selected_departments = dept_options
        st.session_state["selected_departments"] = selected_departments

        st.divider()

        # ── Reset Button ─────────────────────────────────────────────────────
        if st.button("↺ Reset All Filters", use_container_width=True):
            for key in ["age_range", "selected_genders", "selected_payers", "selected_departments"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # ── Active cohort info ───────────────────────────────────────────────
        st.caption(f"**Active Cohort:** {len(df)} total encounters")

    # ── Apply all filters ────────────────────────────────────────────────────
    mask = (
        df["age"].between(age_range[0], age_range[1]) &
        df["gender"].isin(selected_genders) &
        df["payer_name"].isin(selected_payers) &
        df["department"].isin(selected_departments)
    )
    filtered_df = df[mask].copy()

    return filtered_df
