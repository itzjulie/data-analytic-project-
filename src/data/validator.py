import pandas as pd

def validate_analytical_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforces deterministic schema assertions, boundary ranges, and domain typing.
    """
    assert len(df) > 0, "Analytical dataset cannot be empty"
    assert "patient_id" in df.columns, "Missing patient_id column"
    assert "admission_id" in df.columns, "Missing admission_id column"
    
    # Boundary checks
    assert df["age"].between(0, 115).all(), f"Age out of bounds: [{df['age'].min()}, {df['age'].max()}]"
    assert (df["length_of_stay"] >= 1).all(), "Length of stay must be >= 1"
    assert set(df["readmitted_30d"].dropna().unique()).issubset({0, 1}), "Readmission flag must be 0 or 1"
    assert (df["total_charges"] >= 0.0).all(), "Total charges cannot be negative"
    assert (df["out_of_pocket"] >= 0.0).all(), "Out of pocket liabilities cannot be negative"
    
    return df
