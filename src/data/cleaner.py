import pandas as pd

def clean_and_enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw query results, converts datetimes, and adds derived analytical columns.
    """
    df = df.copy()
    
    # Datetime conversions
    if "admission_date" in df.columns:
        df["admission_date"] = pd.to_datetime(df["admission_date"])
    if "discharge_date" in df.columns:
        df["discharge_date"] = pd.to_datetime(df["discharge_date"])
        
    # Categorical ordering
    age_bracket_order = ["<18", "18-35", "36-50", "51-65", ">65"]
    if "age_bracket" in df.columns:
        df["age_bracket"] = pd.Categorical(df["age_bracket"], categories=age_bracket_order, ordered=True)
        
    acuity_order = ["Emergency", "Urgent", "Elective"]
    if "admission_type" in df.columns:
        df["admission_type"] = pd.Categorical(df["admission_type"], categories=acuity_order, ordered=True)
        
    # Derived features
    if "comorbidity_count" not in df.columns and {"hypertension", "diabetes", "cvd", "copd", "ckd"}.issubset(df.columns):
        df["comorbidity_count"] = df["hypertension"] + df["diabetes"] + df["cvd"] + df["copd"] + df["ckd"]
        
    if "is_multimorbid" not in df.columns and "comorbidity_count" in df.columns:
        df["is_multimorbid"] = (df["comorbidity_count"] >= 2).astype(int)
        
    return df
