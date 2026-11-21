# 🏥 Patient Demographic Analysis — Project P104

> **MCA Capstone Project · ABES Engineering College · 2024-25**
> Roll No: `2503201450068` | Candidate: Juli | Mentor: Mr. Dinesh

---

## 📋 Project Overview

An end-to-end, industry-grade **Healthcare Data Analytics** dashboard built with Python 3.12, pandas, Plotly, and Streamlit. The application answers **8 Operational Questions (OQ-01–08)** about patient demographics, clinical comorbidities, length of stay, readmission risk, financial burden, and geographic catchment patterns using **300 synthetic inpatient encounters** from a fictional NCR India hospital.

---

## 🎯 Operational Questions Answered

| OQ | Question | Dashboard Page |
|----|----------|---------------|
| OQ-01 | Age-sex demographic distribution | Demographics |
| OQ-02 | Chronic disease prevalence & co-occurrence | Comorbidities |
| OQ-03 | Inpatient Length of Stay distribution | ALoS & Acuity |
| OQ-04 | Admission acuity (Emergency/Urgent/Elective) | ALoS & Acuity |
| OQ-05 | 30-day hospital readmission rates | Readmission Risk |
| OQ-06 | Patient out-of-pocket financial burden | Financial & Catchment |
| OQ-07 | Geographic catchment & service area | Financial & Catchment |
| OQ-08 | Longitudinal admission trend analysis | Overview |

---

## 🗂️ Folder Structure

```
patient_demographic_analysis/
├── app.py                          # Main landing page (Overview / KPI Dashboard)
├── pages/
│   ├── 01_Demographics.py          # OQ-01 · OQ-07: Demographic profiling
│   ├── 02_Clinical_Comorbidities.py # OQ-02: Disease prevalence & Chi-Square
│   ├── 03_Length_of_Stay_Acuity.py  # OQ-03 · OQ-04: ALoS & acuity
│   ├── 04_Readmission_Risk.py       # OQ-05: 30-day readmission analysis
│   ├── 05_Financial_Payer_Catchment.py # OQ-06 · OQ-07: Finance & geography
│   ├── 06_Data_Explorer.py          # Interactive cohort viewer + CSV export
│   └── 07_Data_Quality_Architecture.py # DQ audit + project info
├── src/
│   ├── data/
│   │   ├── db.py                   # SQLite connection helper (URI read-only)
│   │   ├── validator.py            # Schema validation
│   │   ├── cleaner.py              # Cleaning & enrichment pipeline
│   │   └── loader.py               # @st.cache_data analytical loader
│   ├── analytics/
│   │   ├── statistics.py           # KPI computation, Chi-Square, Kruskal-Wallis
│   │   └── charts.py               # Plotly chart factory (8 OQ-linked charts)
│   └── ui/
│       ├── components.py           # Tailwind iframe components (header, KPI card, alert)
│       └── filters.py              # Shared sidebar filters (st.session_state)
├── data/
│   ├── app.db                      # SQLite database (seed=42, 300 encounters)
│   ├── dim_patients.csv            # 250 fictional Indian patients
│   ├── dim_payers.csv              # 5 insurance payer tiers
│   ├── fact_admissions.csv         # 300 inpatient admissions
│   ├── fact_clinical_diagnoses.csv # 300 clinical diagnosis records
│   ├── fact_billing.csv            # 300 billing records
│   └── v_patient_analytical_master.csv  # 300 × 41-column analytical view
├── tests/
│   ├── test_data.py                # Data layer tests (TC-T-01..04)
│   ├── test_analysis.py            # Analytics tests (TC-T-05..08)
│   └── test_app.py                 # Streamlit AppTest (TC-T-09..10)
├── docs/                           # All 14 SDLC deliverable documents
├── .streamlit/
│   └── config.toml                 # Streamlit theme (navy/blue palette)
├── requirements.txt                # Pinned Python dependencies
└── BUILD_PLAN.md                   # AI-executable build task list
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Web Framework | Streamlit (multipage) |
| CSS / Styling | Tailwind CDN (via `st.components.v1.html` iframe) |
| Database | SQLite 3 (`data/app.db`) |
| Data Wrangling | pandas 2.x, NumPy |
| Statistics | SciPy, statsmodels |
| Visualization | Plotly Express + Graph Objects |
| Testing | pytest + Streamlit AppTest |
| Deployment | Streamlit Community Cloud |

---

## 🚀 Setup & Run

### 1. Prerequisites
- Python 3.12+ installed
- Git installed

### 2. Clone & Install

```bash
# Clone the repository
git clone https://github.com/<your-username>/2503201450068-patient-demographic-analysis.git
cd 2503201450068-patient-demographic-analysis

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux / macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch Dashboard

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** automatically.

### 4. Run Tests

```bash
python -m pytest tests -v
```

Expected: **13 tests pass** in < 30s.

---

## 📊 Key Clinical Findings (Synthetic Data — Seed=42)

| Finding | Value | Significance |
|---------|-------|-------------|
| Dominant age group | 51–65 years | Geriatric-tilt in admissions |
| Overall readmission rate | ~18% | Exceeds 15% HRRP threshold |
| Hypertension prevalence | ~65% | Highest chronic condition burden |
| Multimorbidity (≥2 conditions) | ~42% | Elevated discharge complexity |
| Median ALoS | ~6.5 days | Within clinical norms |
| Urban origin patients | ~60% | Strong urban catchment bias |

> **Note:** All data is **synthetic** (random seed=42) with fictional Indian NCR names and places. No real patient records are used.

---

## 🧪 Test Coverage

| Test File | Test Cases | Covers |
|-----------|-----------|--------|
| `tests/test_data.py` | TC-T-01..04 | DB connection, row counts, PK uniqueness, FK integrity |
| `tests/test_analysis.py` | TC-T-05..08 | KPI formulas, comorbidity matrix, Chi-Square, outlier detection |
| `tests/test_app.py` | TC-T-09..10 | App imports, Streamlit AppTest smoke test |

---

## 📁 Documentation Index

| Step | Deliverable | File |
|------|------------|------|
| 01 | Project Understanding | `docs/01_Project_Understanding.docx` |
| 02 | HMW Problem Framing | `docs/02_HMW_Problem_Framing.docx` |
| 03 | Business Requirements | `docs/03_Needs_Analysis_BR.docx` |
| 04 | RTM | `docs/04_Requirements_Traceability_Matrix.xlsx` |
| 05 | BRD | `docs/05_BRD.docx` |
| 07 | TRD | `docs/07_TRD.docx` |
| 08 | Database Design | `docs/08_Database_Design.xlsx` |
| 09 | ER Diagram | `docs/09_ER_Diagram.docx` + `.png` |
| 10 | Dataset Generation | `docs/10_Dataset_Generation.docx` |
| 11 | User Stories | `docs/11_User_Stories.docx` |
| 12 | UI Framework | `docs/12_UI_Framework.docx` |
| 13 | Test Cases | `docs/13_Test_Cases.docx` |
| 14 | Build Plan | `docs/14_BUILD_PLAN.docx` + `BUILD_PLAN.md` |
| 15 | Build Report | `docs/15_Build_Report.docx` |

---

## 🎓 Academic Information

- **Institution:** ABES Engineering College, Ghaziabad (UP)
- **Programme:** Master of Computer Applications (MCA) — 2nd Year
- **Specialisation:** Data Analytics
- **Roll No:** 2503201450068
- **Mentor:** Mr. Dinesh
- **Academic Year:** 2024-25

---

*Generated by AI-assisted SDLC pipeline · Project P104 · Patient Demographic Analysis*
