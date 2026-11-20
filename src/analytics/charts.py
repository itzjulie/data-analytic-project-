import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Global brand palette
NAVY = "#0F2C59"
SKY_BLUE = "#0284C7"
ROSE = "#EF4444"
EMERALD = "#10B981"
AMBER = "#F59E0B"
SLATE_GRAY = "#64748B"

def plot_population_pyramid(df: pd.DataFrame) -> go.Figure:
    """OQ-01: Bidirectional horizontal bar chart showing demographic age-sex distribution."""
    # Group by age_bracket and gender
    pyramid_df = df.groupby(["age_bracket", "gender"], observed=False).size().reset_index(name="count")
    
    male_counts = []
    female_counts = []
    age_brackets = ["<18", "18-35", "36-50", "51-65", ">65"]
    
    for bracket in age_brackets:
        m_val = pyramid_df[(pyramid_df["age_bracket"] == bracket) & (pyramid_df["gender"] == "Male")]["count"].sum()
        f_val = pyramid_df[(pyramid_df["age_bracket"] == bracket) & (pyramid_df["gender"] == "Female")]["count"].sum()
        male_counts.append(-m_val) # Negative for left side
        female_counts.append(f_val)
        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=age_brackets, x=male_counts,
        name="Male", orientation="h",
        marker=dict(color=NAVY, line=dict(color="#ffffff", width=1)),
        hoverinfo="text",
        hovertext=[f"Age: {b}<br>Male: {-c} patients" for b, c in zip(age_brackets, male_counts)]
    ))
    fig.add_trace(go.Bar(
        y=age_brackets, x=female_counts,
        name="Female", orientation="h",
        marker=dict(color=SKY_BLUE, line=dict(color="#ffffff", width=1)),
        hoverinfo="text",
        hovertext=[f"Age: {b}<br>Female: {c} patients" for b, c in zip(age_brackets, female_counts)]
    ))
    
    max_val = max(abs(min(male_counts or [0])), max(female_counts or [0])) + 5
    fig.update_layout(
        title="<b>Patient Demographic Population Pyramid (Age & Sex Distribution)</b>",
        title_font=dict(size=14, color=NAVY),
        barmode="overlay",
        bargap=0.15,
        xaxis=dict(
            title="Patient Volume",
            tickvals=[-max_val, -max_val//2, 0, max_val//2, max_val],
            ticktext=[str(max_val), str(max_val//2), "0", str(max_val//2), str(max_val)],
            range=[-max_val, max_val],
            gridcolor="#E2E8F0"
        ),
        yaxis=dict(title="Standardized Age Bracket", categoryorder="array", categoryarray=age_brackets),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_comorbidity_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """OQ-02: 5x5 Correlation heatmap of chronic conditions."""
    fig = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale="Blues",
        aspect="auto",
        title="<b>Chronic Comorbidity Correlation Heatmap (Co-occurrence Matrix)</b>"
    )
    fig.update_layout(
        title_font=dict(size=14, color=NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_los_box(df: pd.DataFrame) -> go.Figure:
    """OQ-03: Length of stay box-and-whisker plot with jittered scatter overlay and Tukey fences."""
    fig = px.box(
        df, x="age_bracket", y="length_of_stay", color="age_bracket",
        points="outliers",
        color_discrete_sequence=[NAVY, SKY_BLUE, AMBER, EMERALD, "#8B5CF6"],
        title="<b>Length of Stay (ALoS) Distribution & Outlier Detection by Age Bracket</b>",
        labels={"age_bracket": "Age Bracket", "length_of_stay": "Length of Stay (Days)"}
    )
    # Add 14-day outlier reference line
    fig.add_hline(y=14, line_dash="dash", line_color=ROSE, annotation_text="14-Day Outlier Threshold", annotation_position="top right")
    fig.update_layout(
        title_font=dict(size=14, color=NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        showlegend=False,
        yaxis=dict(gridcolor="#E2E8F0"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_acuity_stacked_bar(df: pd.DataFrame) -> go.Figure:
    """OQ-04: 100% normalized stacked bar chart of admission acuity across age tiers."""
    acuity_df = df.groupby(["age_bracket", "admission_type"], observed=False).size().reset_index(name="count")
    total_per_bracket = acuity_df.groupby("age_bracket", observed=False)["count"].transform("sum")
    acuity_df["pct"] = (acuity_df["count"] / total_per_bracket * 100).round(1)
    
    fig = px.bar(
        acuity_df, x="age_bracket", y="pct", color="admission_type",
        barmode="stack",
        color_discrete_map={"Emergency": ROSE, "Urgent": AMBER, "Elective": SKY_BLUE},
        title="<b>Admission Acuity Breakdown (% Share by Age Bracket)</b>",
        labels={"pct": "Proportion of Cohort (%)", "age_bracket": "Age Bracket", "admission_type": "Acuity Level"}
    )
    fig.update_layout(
        title_font=dict(size=14, color=NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        yaxis=dict(range=[0, 100], gridcolor="#E2E8F0"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_readmission_bars(df: pd.DataFrame) -> go.Figure:
    """OQ-05: Horizontal bar chart of 30-day readmissions with 15% threshold reference line."""
    readmit_df = df.groupby("age_bracket", observed=False)["readmitted_30d"].agg(["mean", "count"]).reset_index()
    readmit_df["pct"] = (readmit_df["mean"] * 100).round(1)
    
    colors = [ROSE if val >= 15.0 else SKY_BLUE for val in readmit_df["pct"]]
    
    fig = go.Figure(go.Bar(
        x=readmit_df["pct"], y=readmit_df["age_bracket"],
        orientation="h",
        marker=dict(color=colors),
        text=[f"{val}%" for val in readmit_df["pct"]],
        textposition="auto"
    ))
    fig.add_vline(x=15.0, line_dash="dash", line_color=ROSE, annotation_text="15% HRRP Penalty Threshold", annotation_position="top right")
    fig.update_layout(
        title="<b>30-Day Readmission Rate (%) by Demographic Cohort</b>",
        title_font=dict(size=14, color=NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(title="Readmission Rate (%)", range=[0, max(25, readmit_df['pct'].max() + 5)], gridcolor="#E2E8F0"),
        yaxis=dict(title="Age Bracket"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_billing_violin(df: pd.DataFrame) -> go.Figure:
    """OQ-06: Violin and box plot comparing total charges vs out-of-pocket liabilities by payer."""
    fig = px.box(
        df, x="payer_tier", y="out_of_pocket", color="payer_tier",
        title="<b>Patient Out-of-Pocket Financial Liability by Payer Tier ($)</b>",
        labels={"payer_tier": "Insurance Payer Category", "out_of_pocket": "Patient Out-of-Pocket ($)"},
        color_discrete_sequence=[EMERALD, NAVY, SKY_BLUE, AMBER, ROSE]
    )
    fig.update_layout(
        title_font=dict(size=14, color=NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        showlegend=False,
        yaxis=dict(gridcolor="#E2E8F0"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_catchment_map(df: pd.DataFrame) -> go.Figure:
    """OQ-07: Regional bubble density plot mapping patient admissions across catchment postal zones."""
    catch_df = df.groupby(["city", "zip_code", "district_type"], observed=False).size().reset_index(name="patient_count")
    
    fig = px.scatter(
        catch_df, x="city", y="patient_count", size="patient_count", color="district_type",
        hover_name="zip_code", size_max=35,
        color_discrete_map={"Urban": NAVY, "Suburban": SKY_BLUE, "Rural": EMERALD},
        title="<b>Patient Catchment Inflow & Density by Municipality & District Type</b>",
        labels={"patient_count": "Inpatient Admissions", "city": "Municipality", "district_type": "District Zone"}
    )
    fig.update_layout(
        title_font=dict(size=14, color=NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        yaxis=dict(gridcolor="#E2E8F0"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_admission_timeline(df: pd.DataFrame) -> go.Figure:
    """OQ-08: Time-series line chart with 30-day moving average overlay."""
    daily = df.groupby("admission_date").size().reset_index(name="daily_admissions")
    daily = daily.sort_values("admission_date")
    daily["sma_30"] = daily["daily_admissions"].rolling(window=30, min_periods=1).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["admission_date"], y=daily["daily_admissions"],
        mode="markers", name="Daily Admissions",
        marker=dict(color=SLATE_GRAY, size=4, opacity=0.4)
    ))
    fig.add_trace(go.Scatter(
        x=daily["admission_date"], y=daily["sma_30"],
        mode="lines", name="30-Day Moving Average",
        line=dict(color=NAVY, width=3)
    ))
    fig.update_layout(
        title="<b>Longitudinal Admission Trends & 30-Day Moving Average (2023-2024)</b>",
        title_font=dict(size=14, color=NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(title="Admission Date", gridcolor="#E2E8F0"),
        yaxis=dict(title="Admission Volume", gridcolor="#E2E8F0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig
