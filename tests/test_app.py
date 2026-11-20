import os
import time
import sqlite3
import pytest
import pandas as pd

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(APP_ROOT, "data", "app.db")
CONFIG_PATH = os.path.join(APP_ROOT, ".streamlit", "config.toml")

def test_streamlit_config_exists_and_valid():
    """TC-T-09: Verify .streamlit/config.toml exists and contains brand palette."""
    assert os.path.exists(CONFIG_PATH), f"Config file missing at {CONFIG_PATH}"
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    assert 'primaryColor = "#0F2C59"' in content, "Primary brand color must be #0F2C59 (Deep Navy)"
    assert 'backgroundColor = "#F8FAFC"' in content, "Background color must be #F8FAFC"

def test_data_load_latency_under_3_seconds():
    """TC-T-10: Verify SQLite query and analytical view ingestion latency < 3.0 seconds."""
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    t0 = time.perf_counter()
    with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as conn:
        df = pd.read_sql_query("SELECT * FROM v_patient_analytical_master", conn)
    latency = time.perf_counter() - t0
    
    assert latency < 3.0, f"Query latency exceeded 3.0s threshold: took {latency:.4f}s"
    assert len(df) >= 150, f"Expected >= 150 rows in analytical view, loaded {len(df)}"

def test_ui_module_imports_and_renders():
    """TC-T-09: Verify UI component library imports cleanly without exceptions."""
    import sys
    if APP_ROOT not in sys.path:
        sys.path.insert(0, APP_ROOT)
    from src.ui import render_tailwind_header, render_kpi_card, render_alert_box
    
    assert callable(render_tailwind_header), "render_tailwind_header must be callable"
    assert callable(render_kpi_card), "render_kpi_card must be callable"
    assert callable(render_alert_box), "render_alert_box must be callable"
