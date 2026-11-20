import numpy as np
import pandas as pd
from scipy import stats

def compute_kpi_summary(df: pd.DataFrame) -> dict:
    """
    Computes overarching executive KPI metrics from filtered patient admissions.
    """
    total_encounters = len(df)
    unique_patients = df["patient_id"].nunique() if total_encounters > 0 else 0
    mean_los = round(float(df["length_of_stay"].mean()), 2) if total_encounters > 0 else 0.0
    median_los = round(float(df["length_of_stay"].median()), 2) if total_encounters > 0 else 0.0
    
    # Non-parametric IQR for Length of Stay
    if total_encounters > 0:
        q25 = float(df["length_of_stay"].quantile(0.25))
        q75 = float(df["length_of_stay"].quantile(0.75))
        iqr_los = round(q75 - q25, 2)
    else:
        q25, q75, iqr_los = 0.0, 0.0, 0.0

    readmit_rate = round(float(df["readmitted_30d"].mean() * 100), 2) if total_encounters > 0 else 0.0
    emergency_ratio = round(float((df["admission_type"] == "Emergency").mean() * 100), 2) if total_encounters > 0 else 0.0
    
    tot_charges = float(df["total_charges"].sum()) if total_encounters > 0 else 0.0
    tot_paid = float(df["insurance_paid"].sum()) if total_encounters > 0 else 0.0
    tot_oop = float(df["out_of_pocket"].sum()) if total_encounters > 0 else 0.0
    coverage_ratio = round(tot_paid / tot_charges, 4) if tot_charges > 0 else 0.0
    median_oop = round(float(df["out_of_pocket"].median()), 2) if total_encounters > 0 else 0.0

    return {
        "total_encounters": total_encounters,
        "unique_patients": unique_patients,
        "mean_los": mean_los,
        "median_los": median_los,
        "q25_los": q25,
        "q75_los": q75,
        "iqr_los": iqr_los,
        "readmission_rate_pct": readmit_rate,
        "emergency_ratio_pct": emergency_ratio,
        "total_charges": tot_charges,
        "total_insurance_paid": tot_paid,
        "total_out_of_pocket": tot_oop,
        "coverage_ratio": coverage_ratio,
        "median_out_of_pocket": median_oop
    }

def detect_los_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags inpatient stay outliers using Tukey's fence rule: LOS > Q3 + 1.5 * IQR.
    """
    if len(df) == 0:
        return df
    df = df.copy()
    q1 = df["length_of_stay"].quantile(0.25)
    q3 = df["length_of_stay"].quantile(0.75)
    iqr = q3 - q1
    upper_fence = q3 + 1.5 * iqr
    df["is_statistical_outlier"] = df["length_of_stay"] > upper_fence
    return df

def compute_comorbidity_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes pairwise co-occurrence correlations across 5 standardized chronic conditions.
    """
    conditions = ["hypertension", "diabetes", "cvd", "copd", "ckd"]
    labels = ["Hypertension", "Diabetes T2", "CVD", "COPD", "CKD"]
    
    sub = df[conditions].copy()
    sub.columns = labels
    corr = sub.corr().round(2)
    return corr

def compute_chi_square_independence(df: pd.DataFrame, factor_col: str, outcome_col: str):
    """
    Executes a Chi-Square Test of Independence between two categorical attributes.
    """
    contingency = pd.crosstab(df[factor_col], df[outcome_col])
    chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
    return {
        "chi2_stat": round(chi2, 3),
        "p_value": round(p_val, 5),
        "dof": dof,
        "is_significant": p_val < 0.05
    }

def compute_moving_average(series: pd.Series, window: int = 30) -> pd.Series:
    """
    Computes rolling Simple Moving Average (SMA) to smooth temporal noise.
    """
    return series.rolling(window=window, min_periods=1).mean()
