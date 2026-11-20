# BUILD PLAN: PATIENT DEMOGRAPHIC ANALYSIS (PROJECT 66)
**Document Version**: 1.0 Baseline | **Author**: Juli (Roll: 2503201450068) | **Mentor**: Gunjan Agrawal  
**Academic Affiliation**: ABES Engineering College, Ghaziabad (MCA 2nd Year Data Analytics)  
**Execution Context**: Step 14 Deliverable (Input Blueprint for Step 15 Build Phase)

---

## 1. Project Summary & Master Artifact Links

### 1.1 Ten-Line Executive Project Summary
1. **Clinical & Operational Problem**: Hospital operations suffer from fragmented reporting and delayed visibility into demographic drivers of inpatient admissions.
2. **Platform Objective**: Project 66 delivers an enterprise-grade demographic intelligence dashboard utilizing Python 3.12, SQLite, and Streamlit.
3. **Core Target Audience**: Designed for Chief Medical Officers, Bed Capacity Managers, Clinical Quality Officers, and Financial Administrators.
4. **Data Warehouse Layer**: Grounded in a 3NF relational SQLite schema (`data/app.db`) tracking 250 patients, 5 payers, and 300 inpatient encounters.
5. **Analytical Precision**: Integrates descriptive statistics, non-parametric ALoS medians, Tukey outlier detection, Chi-Square tests, and logistic odds ratios.
6. **Visualization Suite**: Interactive Plotly charts including bidirectional population pyramids, comorbidity heatmaps, violin plots, and catchment bubble maps.
7. **User Interface Architecture**: Streamlit multipage application enhanced with Tailwind CSS utility classes inside sandboxed iframe components.
8. **Automated Quality Assurance**: 100% automated pytest coverage across database schema integrity, analytical formulas, and UI loading latency (<3.0s).
9. **Zero PHI Compliance**: Exclusively utilizes probabilistic synthetic datasets featuring localized Indian names and NCR regional postal catchment zones.
10. **Delivery & Deployment**: Configured for continuous integration and single-click deployment to Streamlit Community Cloud.

### 1.2 Master Artifact Traceability Links
* [Step 1: Project Understanding & Domain Analysis](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/01_Project_Understanding.docx)
* [Step 2: How Might We (HMW) Problem Framing](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/02_HMW_Problem_Framing.docx)
* [Step 3: Needs Analysis & Business Requirements (BR)](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/03_Needs_Analysis_BR.docx)
* [Step 4: Requirements Traceability Matrix (RTM)](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/04_Requirements_Traceability_Matrix.xlsx)
* [Step 5: Business Requirements Document (BRD)](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/05_BRD.docx)
* [Step 7: Technical Requirements Document (TRD)](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/07_TRD.docx)
* [Step 8: Database Design & Schema Workbook](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/08_Database_Design.xlsx)
* [Step 9: Entity Relationship Diagram & Image](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/09_ER_Diagram.docx)
* [Step 10: Synthetic Dataset Specification & Audit](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/10_Dataset_Generation.docx)
* [Step 11: Agile User Stories & Acceptance Criteria](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/11_User_Stories.docx)
* [Step 12: UI Framework & Wireframe Design](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/12_UI_Framework.docx)
* [Step 13: Functional & Technical Test Cases](file:///C:/Users/HP/.gemini/antigravity/scratch/patient_demographic_analysis/docs/13_Test_Cases.docx)

---

## 2. Final Production Folder Structure

```text
patient_demographic_analysis/
│
├── .streamlit/
│   └── config.toml               # Streamlit brand theme (Deep Navy #0F2C59, Slate Canvas)
│
├── data/
│   ├── app.db                    # Relational SQLite database (tables, indexes, analytical view)
│   ├── patient_demographic_analysis_data.xlsx # Master multi-tab Excel workbook
│   ├── dim_patients.csv          # Master patient demographic dimension (250 records)
│   ├── dim_payers.csv            # Master insurance payer dimension (5 records)
│   ├── fact_admissions.csv       # Inpatient encounters fact table (300 records)
│   ├── fact_clinical_diagnoses.csv # Clinical diagnoses & comorbidity flags (300 records)
│   ├── fact_billing.csv          # Financial billing & insurance claims (300 records)
│   └── v_patient_analytical_master.csv # Denormalized analytical master view (41 columns)
│
├── src/
│   ├── __init__.py
│   ├── generate_data.py          # Probabilistic synthetic data generation engine (Seed=42)
│   ├── ui.py                     # Reusable Tailwind CSS header, KPI card & alert iframe components
│   ├── data/
│   │   ├── __init__.py
│   │   ├── db.py                 # SQLite connection pool with read-only URI handling
│   │   ├── loader.py             # Ingestion service with @st.cache_data decorator
│   │   ├── validator.py          # Schema validation assertions, ranges & null handlers
│   │   └── cleaner.py            # Feature engineering (age binning, comorbidity count)
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── statistics.py         # SciPy/statsmodels statistical computation engine
│   │   └── charts.py             # Plotly interactive charting engine
│   └── ui/
│       ├── __init__.py
│       ├── components.py         # Tailwind CSS iframe wrappers & badge styling
│       └── filters.py            # Global sidebar filter handler with st.session_state
│
├── pages/
│   ├── 01_Demographics.py        # UI-01: Executive Overview & Population Pyramids
│   ├── 02_Clinical_Comorbidities.py # UI-03: Chronic Disease Cross-Tabs & Heatmaps
│   ├── 03_Length_of_Stay_Acuity.py  # UI-04: ALoS Box Plots & Acuity Triage Flow
│   ├── 04_Readmission_Risk.py    # UI-05: 30-Day Readmission Risk Center & Alerts
│   ├── 05_Financial_Payer_Catchment.py # UI-06: Payer Mix & Regional Catchment Map
│   ├── 06_Data_Explorer.py       # UI-07: Interactive Data Query Hub & CSV Export
│   └── 07_Data_Quality_Architecture.py # UI-08: Schema Audit & Academic Metadata
│
├── tests/
│   ├── __init__.py
│   ├── test_data.py              # Database integrity, row counts, PK/FK constraints
│   ├── test_analysis.py          # Mathematical verification on tiny benchmark datasets
│   └── test_app.py               # Latency checks, UI component imports & app tests
│
├── docs/                         # Formal project documentation artifacts (Steps 01-14)
├── app.py                        # Streamlit application main entry point
├── requirements.txt              # Pinned production Python dependencies
├── BUILD_PLAN.md                 # This engineering blueprint
└── README.md                     # GitHub repository documentation & deployment guide
```

---

## 3. Step-by-Step Build Tasks (`BUILD-01` to `BUILD-10`)

### **BUILD-01: Environment Configuration & Pinned Dependencies**
* **Goal**: Establish the local and cloud environment configuration with pinned production libraries.
* **Target Files**: `requirements.txt`, `.streamlit/config.toml`
* **Linked Stories & Features**: Foundation for all User Stories (`US-01` to `US-16`).
* **Exact Prompt for AI**:
  > "Create `requirements.txt` pinning `streamlit==1.35.0`, `pandas>=2.2.0`, `numpy>=1.26.0`, `scipy>=1.13.0`, `statsmodels>=0.14.0`, `plotly>=5.22.0`, `openpyxl>=3.1.0`, `pytest>=8.2.0`. Verify `.streamlit/config.toml` contains `primaryColor = '#0F2C59'`, `backgroundColor = '#F8FAFC'`, `secondaryBackgroundColor = '#FFFFFF'`, `textColor = '#1E293B'`, and `font = 'sans serif'`."
* **How to Check It**: Check that `requirements.txt` exists and install dependencies cleanly.
* **Tests That Must Pass**: `tests/test_app.py::test_streamlit_config_exists_and_valid`

---

### **BUILD-02: Data Ingestion, Caching & Cleaning Engine**
* **Goal**: Build an ACID-compliant data access layer in SQLite with memory caching and validation.
* **Target Files**: `src/data/db.py`, `src/data/loader.py`, `src/data/validator.py`, `src/data/cleaner.py`
* **Linked Stories & Features**: `US-01`, `US-02` | `F-01`, `BR-01`
* **Exact Prompt for AI**:
  > "Implement `src/data/db.py` to open SQLite connections in read-only mode (`file:data/app.db?mode=ro`). In `src/data/loader.py`, write `load_analytical_data()` decorated with `@st.cache_data(ttl=3600, show_spinner=False)` executing a query on `v_patient_analytical_master`. In `src/data/validator.py`, enforce assertions: age between 0 and 115, length_of_stay >= 1, readmitted_30d in {0,1}. In `src/data/cleaner.py`, ensure categorical casting and datetime parsing."
* **How to Check It**: Execute python interactive import and check DataFrame shape is `(300, 41)`.
* **Tests That Must Pass**: `tests/test_data.py::test_sqlite_connection`, `tests/test_data.py::test_table_row_counts`, `tests/test_data.py::test_view_schema_and_column_count`

---

### **BUILD-03: Statistical Computing & Mathematical Engine**
* **Goal**: Implement mathematical aggregations, parametric/non-parametric metrics, and hypothesis tests.
* **Target Files**: `src/analytics/statistics.py`
* **Linked Stories & Features**: `US-03`, `US-05`, `US-08`, `US-09`, `US-12` | `F-02`, `F-03`, `F-05`, `F-06`, `BR-02`, `BR-03`, `BR-05`, `BR-06`
* **Exact Prompt for AI**:
  > "Develop `src/analytics/statistics.py` containing: (1) `compute_kpi_summary(df)` returning total patients, encounters, mean/median ALoS, readmission rate, and coverage ratio; (2) `compute_comorbidity_matrix(df)` returning cross-tabulations and chi2 p-values; (3) `detect_los_outliers(df)` implementing Tukey's IQR fence (`Q3 + 1.5 * IQR`); (4) `compute_readmission_risk(df)` returning cohort rates and odds ratios; and (5) `compute_moving_average(df, window=30)`."
* **How to Check It**: Run unit math against known test vectors.
* **Tests That Must Pass**: `tests/test_analysis.py::test_kpi_formulas_on_known_tiny_dataset`, `tests/test_analysis.py::test_tukey_outlier_detection_logic`, `tests/test_analysis.py::test_chi_square_independence_formula`

---

### **BUILD-04: Plotly Visualization Engine**
* **Goal**: Build reusable, responsive Plotly charting functions implementing the exact designated chart types.
* **Target Files**: `src/analytics/charts.py`
* **Linked Stories & Features**: `US-01`, `US-04`, `US-06`, `US-07`, `US-11`, `US-13`, `US-15`, `US-16` | `F-01` to `F-08`
* **Exact Prompt for AI**:
  > "Write `src/analytics/charts.py` containing: (1) `plot_population_pyramid(df)` generating a bidirectional horizontal bar chart; (2) `plot_comorbidity_heatmap(df)` generating a 5x5 correlation heatmap; (3) `plot_los_box(df)` with jittered scatter overlay and outlier dots; (4) `plot_acuity_stacked_bar(df)` generating a 100% normalized stacked bar; (5) `plot_readmission_bars(df)` with a 15% red reference line; (6) `plot_billing_violin(df)` showing total charges vs out-of-pocket; (7) `plot_catchment_map(df)` generating a regional bubble density plot; and (8) `plot_admission_timeline(df)` with a 30-day moving average overlay."
* **How to Check It**: Check that each function returns a valid `plotly.graph_objects.Figure` object.
* **Tests That Must Pass**: `tests/test_analysis.py::test_moving_average_trend_formula`

---

### **BUILD-05: Reusable Tailwind UI & Filter State Management**
* **Goal**: Implement custom headers, KPI cards, alerts, and shared sidebar state persistence.
* **Target Files**: `src/ui.py`, `src/ui/filters.py`
* **Linked Stories & Features**: `US-02`, `US-10` | `F-01`, `F-05`
* **Exact Prompt for AI**:
  > "In `src/ui.py`, provide `render_tailwind_header(title, subtitle, badge)`, `render_kpi_card(title, value, subtext, badge, color)`, and `render_alert_box(title, message, alert_type)` using `st.components.v1.html` and Tailwind CDN. In `src/ui/filters.py`, implement `render_sidebar_filters(df)` saving `age_range`, `selected_genders`, `selected_payers`, and `selected_departments` in `st.session_state` and returning the filtered DataFrame."
* **How to Check It**: Verify filter state persists across page changes without resetting.
* **Tests That Must Pass**: `tests/test_app.py::test_ui_module_imports_and_renders`

---

### **BUILD-06: Main Application Shell & Overview Page**
* **Goal**: Build the main Streamlit application landing shell and Executive Overview dashboard screen.
* **Target Files**: `app.py`, `pages/01_Demographics.py`
* **Linked Stories & Features**: `US-01`, `US-02` | `UI-01`, `F-01`, `BR-01`
* **Exact Prompt for AI**:
  > "In `app.py`, configure `st.set_page_config(page_title='Patient Demographic Analysis', layout='wide')`. Render the Tailwind header, 4 KPI cards (Total Patients, Total Encounters, Median ALoS, Readmission Rate), sidebar filters, the bidirectional Population Pyramid, and summary table. Duplicate clean entry into `pages/01_Demographics.py`."
* **How to Check It**: Run `streamlit run app.py` and verify screen loads in $<2$s with interactive charts.
* **Tests That Must Pass**: `tests/test_app.py::test_data_load_latency_under_3_seconds`

---

### **BUILD-07: Clinical Comorbidities & Inpatient Capacity Screens**
* **Goal**: Deliver the clinical epidemiological matrix, comorbidity heatmap, ALoS outlier analysis, and acuity flow screens.
* **Target Files**: `pages/02_Clinical_Comorbidities.py`, `pages/03_Length_of_Stay_Acuity.py`
* **Linked Stories & Features**: `US-03`, `US-04`, `US-05`, `US-06`, `US-07`, `US-08` | `UI-03`, `UI-04`, `F-02`, `F-03`, `F-04`, `BR-02`, `BR-03`, `BR-04`
* **Exact Prompt for AI**:
  > "Build `pages/02_Clinical_Comorbidities.py` displaying prevalence KPI cards, condition cross-tabulation table, and 5x5 comorbidity correlation heatmap. Build `pages/03_Length_of_Stay_Acuity.py` rendering parametric/non-parametric stay metrics, ALoS box plot with Tukey outlier fences, an interactive table of prolonged stays (>14d), and 100% stacked acuity triage bars."
* **How to Check It**: Navigate to both pages in browser; verify box plot displays outliers and heatmap renders.
* **Tests That Must Pass**: Functional tests `TC-F-03`, `TC-F-04`, `TC-F-05`, `TC-F-06`, `TC-F-07`

---

### **BUILD-08: Quality Readmission Center & Financial Catchment Screens**
* **Goal**: Build the clinical quality 30-day readmission monitoring center, threshold alerting, financial payer distribution, and regional maps.
* **Target Files**: `pages/04_Readmission_Risk.py`, `pages/05_Financial_Payer_Catchment.py`
* **Linked Stories & Features**: `US-09`, `US-10`, `US-11`, `US-12`, `US-13`, `US-14` | `UI-05`, `UI-06`, `F-05`, `F-06`, `F-07`, `BR-05`, `BR-06`, `BR-07`
* **Exact Prompt for AI**:
  > "Develop `pages/04_Readmission_Risk.py` featuring dynamic crimson alert banner if cohort readmission exceeds 15%, readmission rate bar chart with 15% reference line, and logistic odds ratio breakdown. Develop `pages/05_Financial_Payer_Catchment.py` rendering violin plots of total charges vs out-of-pocket, payer reimbursement table, and regional postal bubble density map."
* **How to Check It**: Check that the warning banner appears for senior patients (>65) and bubble map displays Ghaziabad/Noida/Meerut clusters.
* **Tests That Must Pass**: Functional tests `TC-F-08`, `TC-F-09`, `TC-F-10`, `TC-F-11`

---

### **BUILD-09: Data Explorer & Quality Diagnostic Hub**
* **Goal**: Build self-service tabular data explorer, CSV download buttons, and automated data quality diagnostic screen.
* **Target Files**: `pages/06_Data_Explorer.py`, `pages/07_Data_Quality_Architecture.py`
* **Linked Stories & Features**: `UI-07`, `UI-08` | Analytical Self-Service & Architecture Verification
* **Exact Prompt for AI**:
  > "Create `pages/06_Data_Explorer.py` with multi-column dataframe search, row limit slider, and 'Download Filtered Data (CSV)' button. Create `pages/07_Data_Quality_Architecture.py` displaying live SQLite row counts, schema foreign key verification status, range validation badges, and candidate/mentor metadata box."
* **How to Check It**: Download filtered CSV and confirm it matches filtered active rows; verify all quality badges display 'PASSED'.
* **Tests That Must Pass**: Functional test `TC-F-12`, Technical test `TC-T-02`

---

### **BUILD-10: Final Verification, Documentation & Deployment Packaging**
* **Goal**: Execute full test suite, verify 100% test pass rate, write production `README.md`, and stage for Streamlit Community Cloud.
* **Target Files**: `README.md`, Git configuration
* **Linked Stories & Features**: All User Stories & Features
* **Exact Prompt for AI**:
  > "Run `python -m pytest tests -v` and confirm 13/13 tests pass. Create a comprehensive `README.md` containing project title, academic metadata (Juli, Roll: 2503201450068, Mentor: Gunjan Agrawal, ABES), system architecture overview, local installation instructions, test execution guide, and live Streamlit Cloud URL."
* **How to Check It**: All pytest tests exit with code 0. README renders cleanly.
* **Tests That Must Pass**: Complete test suite (13/13 tests passed).

---

## 4. Definition of Done (DoD)

A task or release increment is considered **DONE** only when all of the following criteria are satisfied:
1. **Requirements Coverage**: All 8 Business Requirements (`BR-01` to `BR-08`) and all 8 Core Features (`F-01` to `F-08`) are fully implemented and verified.
2. **Quality Benchmark**: 100% of automated pytest tests (13/13) pass cleanly with zero errors or failures.
3. **Execution Latency**: Global dashboard queries and page rendering complete in $<2.0$ seconds on standard datasets.
4. **Defensive Stability**: Zero unhandled exceptions or Python tracebacks occur during empty filter selections or rapid parameter adjustments.
5. **Aesthetic Compliance**: All screens feature the unified Deep Navy theme (`#0F2C59`), Tailwind CSS headers, metric cards, and responsive layout.
6. **Documentation Completeness**: Production `README.md` and Word deliverable (`docs/14_BUILD_PLAN.docx`) are saved and up to date.

---

## 5. Execution Commands Quick Reference

```bash
# 1. Environment Installation
python -m pip install -r requirements.txt

# 2. Synthetic Dataset Regeneration (Optional, if app.db needs re-creation)
python src/generate_data.py

# 3. Automated Test Suite Execution
python -m pytest tests -v

# 4. Local Web Application Launch
streamlit run app.py
```

---

## 6. Authoritative Viva Defense Preparation (Top 10 Questions & Answers)

1. **Q: What is the core business objective of Project 66?**  
   *A*: To provide hospital leadership and clinical analysts with an automated demographic analytics dashboard that segments patients by age, gender, geography, insurance, and comorbidities to optimize inpatient bed turnaround, predict emergency surges, and reduce 30-day readmissions.

2. **Q: Why was SQLite selected instead of a server-hosted RDBMS like MySQL or PostgreSQL?**  
   *A*: SQLite is serverless, zero-configuration, and ACID-compliant. The entire database is encapsulated in a single file (`data/app.db`) that deploys directly into containerized environments like Streamlit Community Cloud without external connection latency or database hosting costs.

3. **Q: Why are Length of Stay (ALoS) differences evaluated using non-parametric statistical methods?**  
   *A*: Healthcare length of stay data is heavily right-skewed; most patients stay 2 to 5 days, while a long-tail minority remain hospitalized for weeks. Non-parametric methods (Kruskal-Wallis and Mann-Whitney U) evaluate rank distributions rather than means, avoiding false statistical conclusions caused by outliers.

4. **Q: How does the system detect outlier hospitalizations?**  
   *A*: Using Tukey's Interquartile Range (IQR) fence rule. An inpatient stay is flagged as an outlier if $\text{Length of Stay} > Q_3 + 1.5 \times \text{IQR}$, which cleanly identifies complex hospitalizations exceeding 14 days.

5. **Q: What clinical patterns are mathematically built into the synthetic data?**  
   *A*: (1) Age-comorbidity gradient: senior cohorts have $>60\%$ hypertension prevalence; (2) High emergency dependency in seniors ($>50\%$); (3) 30-day readmission concentration among multi-morbid patients ($20.0\%$); (4) Payer reimbursement disparities (Medicaid 90% vs Self-Pay 0%); (5) Winter respiratory surges.

6. **Q: How does the system handle patient privacy and HIPAA compliance?**  
   *A*: The platform operates under an absolute Zero-PHI constraint (A-03). All names, contact details, and clinical encounters are synthetically generated using probabilistic models and localized Indian naming conventions (seed=42).

7. **Q: What is the purpose of `@st.cache_data` in the ingestion layer?**  
   *A*: It caches serializable DataFrames in memory with a Time-To-Live of 3,600 seconds. Subsequent page navigation or filter adjustments query the cached memory copy rather than reading from disk, cutting UI latency from 2 seconds to $<150$ milliseconds.

8. **Q: Why is Tailwind CSS embedded inside an iframe rather than injected via `unsafe_allow_html`?**  
   *A*: An `<iframe>` provides an isolated browsing context and separate DOM. This allows Tailwind utility classes to style modern headers and metric cards without leaking styles into Streamlit's native layout or causing XSS vulnerabilities.

9. **Q: How does the dashboard alert clinicians to high readmission risk?**  
   *A*: When a cohort's evaluated 30-day readmission rate exceeds the 15% quality threshold, the UI dynamically renders a crimson warning banner and applies color-coded reference markers to highlight regulatory penalty risk under Medicare HRRP programs.

10. **Q: How are requirements tracked from inception to verification?**  
    *A*: Through the formal Requirements Traceability Matrix (RTM), which links each Operational Question (`OQ`) to its Stakeholder (`SH`), HMW Statement (`HMW`), Business Requirement (`BR`), Feature (`F`), Functional Requirement (`FR`), User Story (`US`), UI Screen (`UI`), and Test Cases (`TC-F` & `TC-T`).
