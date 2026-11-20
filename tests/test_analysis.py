import numpy as np
import pandas as pd
import pytest
from scipy import stats

def compute_kpis(df: pd.DataFrame) -> dict:
    """Helper function to calculate core analytical KPIs."""
    total_encounters = len(df)
    mean_los = round(float(df["length_of_stay"].mean()), 2) if total_encounters > 0 else 0.0
    median_los = round(float(df["length_of_stay"].median()), 2) if total_encounters > 0 else 0.0
    readmit_rate = round(float(df["readmitted_30d"].mean() * 100), 2) if total_encounters > 0 else 0.0
    
    tot_charges = df["total_charges"].sum()
    tot_paid = df["insurance_paid"].sum()
    coverage_ratio = round(float(tot_paid / tot_charges), 4) if tot_charges > 0 else 0.0
    
    return {
        "total_encounters": total_encounters,
        "mean_los": mean_los,
        "median_los": median_los,
        "readmission_rate_pct": readmit_rate,
        "coverage_ratio": coverage_ratio
    }

def detect_outliers_iqr(series: pd.Series) -> pd.Series:
    """Tukey's IQR method for outlier detection."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    upper_fence = q3 + 1.5 * iqr
    return series > upper_fence

def test_kpi_formulas_on_known_tiny_dataset():
    """TC-T-05: Verify KPI mathematical formulas against known manual calculation."""
    tiny_data = pd.DataFrame({
        "admission_id": ["ADM-1", "ADM-2", "ADM-3", "ADM-4"],
        "length_of_stay": [2, 4, 6, 12],
        "readmitted_30d": [0, 1, 0, 1],
        "total_charges": [1000.0, 2000.0, 3000.0, 4000.0],
        "insurance_paid": [800.0, 1600.0, 2400.0, 3200.0]
    })
    
    kpis = compute_kpis(tiny_data)
    
    # Assert exact math:
    # Mean LOS = (2 + 4 + 6 + 12) / 4 = 24 / 4 = 6.0
    assert kpis["mean_los"] == 6.0
    # Median LOS = (4 + 6) / 2 = 5.0
    assert kpis["median_los"] == 5.0
    # Readmission Rate = 2 / 4 = 50.0%
    assert kpis["readmission_rate_pct"] == 50.0
    # Coverage Ratio = (800+1600+2400+3200) / 10000 = 8000 / 10000 = 0.8000
    assert kpis["coverage_ratio"] == 0.8000

def test_tukey_outlier_detection_logic():
    """TC-T-07: Verify Tukey's fence outlier identification logic."""
    data = pd.Series([3, 4, 4, 5, 5, 5, 6, 6, 7, 25]) # 25 is an extreme outlier
    outliers = detect_outliers_iqr(data)
    assert outliers.sum() == 1, "Expected exactly 1 outlier detected"
    assert outliers.iloc[-1] == True, "The last element (25) must be flagged as outlier"

def test_chi_square_independence_formula():
    """TC-T-06: Verify Chi-Square calculation formula and p-value output."""
    # 2x2 contingency table (e.g., Senior vs Non-Senior x Hypertension vs Normal)
    contingency = np.array([
        [68, 32], # Senior: 68 Hypertensive, 32 Normal
        [15, 85]  # Young: 15 Hypertensive, 85 Normal
    ])
    chi2, p_val, dof, expected = stats.chi2_contingency(contingency)
    assert chi2 > 0.0, "Chi-square statistic must be positive"
    assert dof == 1, "Degrees of freedom for 2x2 table must be 1"
    assert p_val < 0.001, "Significantly higher hypertension among seniors must yield p < 0.001"

def test_moving_average_trend_formula():
    """TC-T-08: Verify rolling moving average smoothing."""
    series = pd.Series([10.0] * 30 + [20.0] * 30)
    sma = series.rolling(window=30, min_periods=1).mean()
    assert sma.iloc[29] == 10.0
    assert sma.iloc[-1] == 20.0
