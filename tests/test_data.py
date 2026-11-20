import os
import sqlite3
import pytest
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")

@pytest.fixture
def db_conn():
    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    yield conn
    conn.close()

def test_sqlite_connection(db_conn):
    """TC-T-01: Verify SQLite database connectivity and FK pragma."""
    cur = db_conn.cursor()
    cur.execute("PRAGMA foreign_keys;")
    fk_status = cur.fetchone()[0]
    assert fk_status == 1, "Foreign keys must be enabled (PRAGMA foreign_keys = 1)"

def test_table_row_counts(db_conn):
    """TC-T-02: Verify minimum row counts across masters and fact tables."""
    cur = db_conn.cursor()
    cur.execute("SELECT count(*) FROM dim_patients")
    patients_count = cur.fetchone()[0]
    assert patients_count >= 200, f"Expected >= 200 patients, found {patients_count}"

    cur.execute("SELECT count(*) FROM dim_payers")
    payers_count = cur.fetchone()[0]
    assert payers_count == 5, f"Expected 5 payers, found {payers_count}"

    cur.execute("SELECT count(*) FROM fact_admissions")
    admissions_count = cur.fetchone()[0]
    assert admissions_count >= 150, f"Expected >= 150 admissions, found {admissions_count}"

    cur.execute("SELECT count(*) FROM fact_clinical_diagnoses")
    dx_count = cur.fetchone()[0]
    assert dx_count == admissions_count, "Clinical diagnoses must match admissions count (1:1)"

    cur.execute("SELECT count(*) FROM fact_billing")
    billing_count = cur.fetchone()[0]
    assert billing_count == admissions_count, "Billing records must match admissions count (1:1)"

def test_primary_key_uniqueness(db_conn):
    """TC-T-02: Verify Primary Key uniqueness across all tables."""
    tables_pk = [
        ("dim_patients", "patient_id"),
        ("dim_payers", "payer_id"),
        ("fact_admissions", "admission_id"),
        ("fact_clinical_diagnoses", "diagnosis_id"),
        ("fact_billing", "billing_id")
    ]
    cur = db_conn.cursor()
    for table, pk in tables_pk:
        cur.execute(f"SELECT count({pk}), count(DISTINCT {pk}) FROM {table}")
        total, distinct = cur.fetchone()
        assert total == distinct, f"Duplicate Primary Keys detected in table {table} on column {pk}"

def test_foreign_key_integrity(db_conn):
    """TC-T-03: Verify zero foreign key violations using SQLite PRAGMA."""
    cur = db_conn.cursor()
    cur.execute("PRAGMA foreign_key_check;")
    violations = cur.fetchall()
    assert len(violations) == 0, f"Foreign key integrity violations detected: {violations}"

def test_range_and_domain_constraints(db_conn):
    """TC-T-04: Verify domain range constraints (age, length of stay, binary flags)."""
    cur = db_conn.cursor()
    # Age range
    cur.execute("SELECT min(age), max(age) FROM dim_patients")
    min_age, max_age = cur.fetchone()
    assert 0 <= min_age and max_age <= 115, f"Invalid age bounds: [{min_age}, {max_age}]"

    # Length of Stay >= 1
    cur.execute("SELECT min(length_of_stay) FROM fact_admissions")
    min_los = cur.fetchone()[0]
    assert min_los >= 1, f"Length of stay must be >= 1, found {min_los}"

    # Readmitted flag in {0, 1}
    cur.execute("SELECT DISTINCT readmitted_30d FROM fact_admissions")
    flags = [r[0] for r in cur.fetchall()]
    assert set(flags).issubset({0, 1}), f"Readmission flags must be in {{0, 1}}, found {flags}"

    # Coverage ratio in [0.0, 1.0]
    cur.execute("SELECT min(claim_coverage_ratio), max(claim_coverage_ratio) FROM fact_billing")
    min_cov, max_cov = cur.fetchone()
    assert 0.0 <= min_cov and max_cov <= 1.0, f"Coverage ratio out of bounds: [{min_cov}, {max_cov}]"

def test_view_schema_and_column_count(db_conn):
    """TC-T-01: Verify analytical view exists and contains about 30-40 columns (41 columns)."""
    df = pd.read_sql_query("SELECT * FROM v_patient_analytical_master LIMIT 5", db_conn)
    assert 35 <= len(df.columns) <= 45, f"Analytical view must contain ~30-40 columns, found {len(df.columns)}"
    required_cols = [
        "admission_id", "patient_id", "age", "age_bracket", "gender", "length_of_stay",
        "primary_diagnosis", "hypertension", "diabetes", "total_charges", "out_of_pocket"
    ]
    for col in required_cols:
        assert col in df.columns, f"Required column '{col}' missing from analytical master view"
