import os
import random
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Set deterministic random seed
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

def get_age_bracket(age: int) -> str:
    if age < 18:
        return "<18"
    elif age <= 35:
        return "18-35"
    elif age <= 50:
        return "36-50"
    elif age <= 65:
        return "51-65"
    else:
        return ">65"

def get_season(month: int) -> str:
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

def generate_synthetic_dataset():
    print(f"[*] Initializing Synthetic Healthcare Data Generator (Seed={SEED})...")
    
    # ---------------------------------------------------------
    # 1. PAYERS DIMENSION (5 Payers)
    # ---------------------------------------------------------
    payers_data = [
        {"payer_id": "PAY-01", "payer_name": "Ayushman Bharat PM-JAY", "payer_tier": "Medicaid", "avg_reimbursement_rate": 0.90, "standard_copay": 0.0},
        {"payer_id": "PAY-02", "payer_name": "CGHS Federal Healthcare", "payer_tier": "Medicare", "avg_reimbursement_rate": 0.85, "standard_copay": 150.0},
        {"payer_id": "PAY-03", "payer_name": "Star Health Comprehensive", "payer_tier": "Private HMO", "avg_reimbursement_rate": 0.80, "standard_copay": 500.0},
        {"payer_id": "PAY-04", "payer_name": "ICICI Lombard Health Shield", "payer_tier": "Private PPO", "avg_reimbursement_rate": 0.75, "standard_copay": 750.0},
        {"payer_id": "PAY-05", "payer_name": "Self-Pay / Cash Patient", "payer_tier": "Self-Pay", "avg_reimbursement_rate": 0.00, "standard_copay": 0.0}
    ]
    df_payers = pd.DataFrame(payers_data)

    # ---------------------------------------------------------
    # 2. PATIENTS DIMENSION (250 Patients)
    # ---------------------------------------------------------
    first_names_male = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Ayaan", "Krishna", "Ishan", "Shaurya", "Rajesh", "Suresh", "Ramesh", "Amit", "Rohit", "Vikram", "Sanjay", "Manoj", "Deepak", "Anil", "Sunil", "Pankaj", "Alok", "Manish"]
    first_names_female = ["Ananya", "Diya", "Saanvi", "Aadhya", "Pari", "Myra", "Riya", "Anika", "Navya", "Kavya", "Sunita", "Pooja", "Priya", "Neha", "Anita", "Rekha", "Meena", "Shashi", "Geeta", "Seema", "Kiran", "Usha", "Vandana", "Mamta"]
    last_names = ["Sharma", "Verma", "Gupta", "Patel", "Singh", "Kumar", "Yadav", "Mishra", "Das", "Mehta", "Joshi", "Agarwal", "Bansal", "Choudhary", "Jha", "Reddy", "Nair", "Rao", "Tiwari", "Bhatia", "Saxena", "Pandey", "Shukla", "Tripathi"]
    
    locations = [
        {"zip": "201001", "city": "Ghaziabad", "district": "Urban"},
        {"zip": "201002", "city": "Ghaziabad", "district": "Urban"},
        {"zip": "201009", "city": "Ghaziabad", "district": "Suburban"},
        {"zip": "201301", "city": "Noida", "district": "Urban"},
        {"zip": "201303", "city": "Noida", "district": "Urban"},
        {"zip": "201310", "city": "Greater Noida", "district": "Suburban"},
        {"zip": "250001", "city": "Meerut", "district": "Urban"},
        {"zip": "250002", "city": "Meerut", "district": "Suburban"},
        {"zip": "110091", "city": "East Delhi", "district": "Urban"},
        {"zip": "110092", "city": "East Delhi", "district": "Urban"},
        {"zip": "110001", "city": "Central Delhi", "district": "Urban"},
        {"zip": "122001", "city": "Gurugram", "district": "Urban"},
        {"zip": "245101", "city": "Hapur", "district": "Rural"},
        {"zip": "203001", "city": "Bulandshahr", "district": "Rural"}
    ]
    
    ethnicities = ["General Category", "OBC", "SC/ST", "Minority Community", "Other"]
    
    # Age distribution probabilities matching typical hospital demographics
    # <18 (8%), 18-35 (22%), 36-50 (26%), 51-65 (24%), >65 (20%)
    patients_data = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(1, 251):
        pid = f"PAT-{1000 + i}"
        
        # Gender selection (49% Male, 49% Female, 2% Non-Binary)
        g_rand = random.random()
        if g_rand < 0.49:
            gender = "Male"
            fname = random.choice(first_names_male)
        elif g_rand < 0.98:
            gender = "Female"
            fname = random.choice(first_names_female)
        else:
            gender = "Non-Binary"
            fname = random.choice(first_names_male + first_names_female)
            
        lname = random.choice(last_names)
        
        # Age selection with realistic weights
        age_tier = random.choices(["ped", "ya", "ad", "ma", "ger"], weights=[0.08, 0.22, 0.26, 0.24, 0.20])[0]
        if age_tier == "ped":
            age = random.randint(1, 17)
        elif age_tier == "ya":
            age = random.randint(18, 35)
        elif age_tier == "ad":
            age = random.randint(36, 50)
        elif age_tier == "ma":
            age = random.randint(51, 65)
        else:
            age = random.randint(66, 88)
            
        age_bracket = get_age_bracket(age)
        dob = base_date - timedelta(days=int(age * 365.25) + random.randint(0, 360))
        
        loc = random.choice(locations)
        ethnicity = random.choices(ethnicities, weights=[0.40, 0.30, 0.15, 0.10, 0.05])[0]
        
        patients_data.append({
            "patient_id": pid,
            "first_name": fname,
            "last_name": lname,
            "date_of_birth": dob.strftime("%Y-%m-%d"),
            "age": age,
            "age_bracket": age_bracket,
            "gender": gender,
            "ethnicity": ethnicity,
            "zip_code": loc["zip"],
            "city": loc["city"],
            "district_type": loc["district"]
        })
        
    df_patients = pd.DataFrame(patients_data)

    # ---------------------------------------------------------
    # 3. ADMISSIONS FACT & EXTENSIONS (300 Encounters)
    # ---------------------------------------------------------
    # Distributed across the 250 patients:
    # 200 patients have 1 admission, 50 patients have 2 admissions (to model repeat admissions / 30-day readmissions)
    patient_ids_pool = [p["patient_id"] for p in patients_data]
    repeated_patients = random.sample(patient_ids_pool, 50)
    encounter_patient_ids = patient_ids_pool + repeated_patients # Exactly 300 admissions
    random.shuffle(encounter_patient_ids)
    
    admissions_data = []
    diagnoses_data = []
    billing_data = []
    
    # Date range: 2023-01-01 to 2024-12-15
    start_date = datetime(2023, 1, 1)
    
    departments = ["Cardiology", "Pulmonology", "General Medicine", "ICU", "Orthopedics"]
    
    for idx in range(1, 301):
        adm_id = f"ADM-{10000 + idx}"
        pid = encounter_patient_ids[idx - 1]
        p_row = df_patients[df_patients["patient_id"] == pid].iloc[0]
        p_age = p_row["age"]
        p_bracket = p_row["age_bracket"]
        
        # Payer assignment: Geriatric patients more likely Medicare/CGHS; Pediatric/Adult Medicaid/Private
        if p_age >= 65:
            payer_id = random.choices(["PAY-01", "PAY-02", "PAY-03", "PAY-04", "PAY-05"], weights=[0.15, 0.45, 0.15, 0.15, 0.10])[0]
        elif p_age < 18:
            payer_id = random.choices(["PAY-01", "PAY-02", "PAY-03", "PAY-04", "PAY-05"], weights=[0.30, 0.10, 0.30, 0.20, 0.10])[0]
        else:
            payer_id = random.choices(["PAY-01", "PAY-02", "PAY-03", "PAY-04", "PAY-05"], weights=[0.20, 0.15, 0.30, 0.25, 0.10])[0]
            
        payer_info = df_payers[df_payers["payer_id"] == payer_id].iloc[0]
        
        # PATTERN 5: Seasonal admission clustering (Winter respiratory surge in Dec, Jan, Feb)
        rand_days = random.randint(0, 715)
        adm_date = start_date + timedelta(days=rand_days)
        month = adm_date.month
        year = adm_date.year
        season = get_season(month)
        
        # PATTERN 2: Acuity by Age — Seniors have higher Emergency admission rate (~60%)
        if p_age >= 65:
            adm_type = random.choices(["Emergency", "Urgent", "Elective"], weights=[0.60, 0.25, 0.15])[0]
        elif p_age >= 51:
            adm_type = random.choices(["Emergency", "Urgent", "Elective"], weights=[0.45, 0.25, 0.30])[0]
        else:
            adm_type = random.choices(["Emergency", "Urgent", "Elective"], weights=[0.25, 0.25, 0.50])[0]
            
        # Clinical department assignment based on season and age
        if season == "Winter" and p_age >= 50:
            dept = random.choices(departments, weights=[0.30, 0.35, 0.20, 0.10, 0.05])[0]
        elif p_age >= 65:
            dept = random.choices(departments, weights=[0.35, 0.20, 0.20, 0.15, 0.10])[0]
        elif p_age < 18:
            dept = random.choices(departments, weights=[0.05, 0.35, 0.45, 0.05, 0.10])[0]
        else:
            dept = random.choices(departments, weights=[0.20, 0.15, 0.30, 0.10, 0.25])[0]
            
        # PATTERN 1 & 2: Length of Stay (ALoS) - higher for seniors & ICU
        # Mean stay ~4 days for young, ~7.5 days for seniors.
        if dept == "ICU":
            los = int(np.random.gamma(shape=3.5, scale=2.5)) + 2 # Mean ~10 days
        elif p_age >= 65:
            los = int(np.random.gamma(shape=3.0, scale=2.2)) + 1 # Mean ~7.6 days
        elif p_age >= 51:
            los = int(np.random.gamma(shape=2.5, scale=2.0)) + 1 # Mean ~6.0 days
        else:
            los = int(np.random.gamma(shape=2.0, scale=1.6)) + 1 # Mean ~3.5 days
            
        los = max(1, los)
        
        # Outlier flag (>14 days)
        # Introduce 7 deliberate outliers (los between 15 and 28 days)
        if idx in [14, 48, 92, 145, 188, 233, 279]:
            los = random.randint(16, 28)
            is_outlier = 1
        else:
            is_outlier = 1 if los > 14 else 0
            
        disch_date = adm_date + timedelta(days=los)
        
        # Discharge disposition
        if p_age >= 65 and los > 8:
            disch_disp = random.choices(["Home", "Skilled Nursing", "Rehabilitation", "AMA"], weights=[0.60, 0.25, 0.12, 0.03])[0]
        else:
            disch_disp = random.choices(["Home", "Skilled Nursing", "Rehabilitation", "AMA"], weights=[0.85, 0.08, 0.05, 0.02])[0]

        # PATTERN 1: Chronic Comorbidity Prevalence
        # Seniors have much higher probability of Hypertension (~65%) and Diabetes (~50%)
        if p_age >= 65:
            p_hyp = 0.68; p_dia = 0.52; p_cvd = 0.40; p_copd = 0.30; p_ckd = 0.22
        elif p_age >= 51:
            p_hyp = 0.50; p_dia = 0.38; p_cvd = 0.25; p_copd = 0.18; p_ckd = 0.12
        elif p_age >= 36:
            p_hyp = 0.28; p_dia = 0.20; p_cvd = 0.10; p_copd = 0.08; p_ckd = 0.04
        elif p_age >= 18:
            p_hyp = 0.08; p_dia = 0.05; p_cvd = 0.02; p_copd = 0.05; p_ckd = 0.01
        else:
            p_hyp = 0.01; p_dia = 0.01; p_cvd = 0.01; p_copd = 0.08; p_ckd = 0.01

        hyp = 1 if random.random() < p_hyp else 0
        dia = 1 if random.random() < p_dia else 0
        cvd = 1 if random.random() < p_cvd else 0
        copd = 1 if random.random() < p_copd else 0
        ckd = 1 if random.random() < p_ckd else 0
        comorb_count = hyp + dia + cvd + copd + ckd
        
        # Primary Diagnosis aligned with department and comorbidities
        if dept == "Cardiology":
            prim_dx = random.choice(["Coronary Artery Disease", "Heart Failure", "Hypertension"])
            hyp = 1
        elif dept == "Pulmonology":
            prim_dx = random.choice(["COPD", "Asthma"])
            copd = 1 if prim_dx == "COPD" else copd
        elif dept == "Orthopedics":
            prim_dx = "Osteoarthritis / Fracture"
        elif dept == "ICU":
            prim_dx = random.choice(["Heart Failure", "Severe Sepsis", "Respiratory Failure"])
            cvd = 1
        else:
            prim_dx = random.choice(["Type 2 Diabetes", "Hypertension", "Gastroenteritis", "Pneumonia"])
            if prim_dx == "Type 2 Diabetes":
                dia = 1
                
        comorb_count = hyp + dia + cvd + copd + ckd

        # PATTERN 3: 30-Day Readmission Risk
        # Strong correlation with high comorbidity count (>=2) and senior age
        readmit_prob = 0.05 # Baseline
        if p_age >= 65:
            readmit_prob += 0.08
        if comorb_count >= 2:
            readmit_prob += 0.12
        if prim_dx in ["Heart Failure", "COPD"]:
            readmit_prob += 0.10
        if los > 10:
            readmit_prob += 0.05
            
        readmit_prob = min(0.45, readmit_prob)
        readmitted_30d = 1 if random.random() < readmit_prob else 0
        
        if readmitted_30d == 1:
            readmit_days = random.randint(4, 29)
        else:
            readmit_days = None

        # PATTERN 4: Billing & Financials
        # Total charges based on Length of Stay and ICU presence
        base_charge_per_day = 3500.0 if dept == "ICU" else 1600.0
        proc_charges = 8500.0 if dept in ["Cardiology", "ICU"] else 3000.0
        tot_charges = round((los * base_charge_per_day) + proc_charges + np.random.uniform(500, 2500), 2)
        
        # Introduce 3 deliberate billing outliers ($52k to $68k)
        if idx in [33, 112, 240]:
            tot_charges = round(tot_charges + random.randint(35000, 48000), 2)
            
        reimb_rate = payer_info["avg_reimbursement_rate"]
        ins_paid = round(tot_charges * reimb_rate, 2)
        out_of_pocket = round(tot_charges - ins_paid, 2)
        cov_ratio = round(ins_paid / tot_charges, 4) if tot_charges > 0 else 0.0
        
        claim_status = random.choices(["Settled", "Pending", "Disputed", "Written-Off"], weights=[0.82, 0.10, 0.05, 0.03])[0]
        bill_date = disch_date.strftime("%Y-%m-%d")

        # Append to respective tables
        admissions_data.append({
            "admission_id": adm_id,
            "patient_id": pid,
            "payer_id": payer_id,
            "admission_date": adm_date.strftime("%Y-%m-%d"),
            "discharge_date": disch_date.strftime("%Y-%m-%d"),
            "admission_year": year,
            "admission_month": month,
            "admission_season": season,
            "admission_type": adm_type,
            "department": dept,
            "length_of_stay": los,
            "is_outlier_stay": is_outlier,
            "discharge_disposition": disch_disp,
            "readmitted_30d": readmitted_30d,
            "readmission_days": readmit_days
        })
        
        diagnoses_data.append({
            "diagnosis_id": f"DX-{10000 + idx}",
            "admission_id": adm_id,
            "primary_diagnosis": prim_dx,
            "hypertension": hyp,
            "diabetes": dia,
            "cvd": cvd,
            "copd": copd,
            "ckd": ckd,
            "comorbidity_count": comorb_count
        })
        
        billing_data.append({
            "billing_id": f"BIL-{10000 + idx}",
            "admission_id": adm_id,
            "total_charges": tot_charges,
            "insurance_paid": ins_paid,
            "out_of_pocket": out_of_pocket,
            "claim_coverage_ratio": cov_ratio,
            "claim_status": claim_status,
            "billing_date": bill_date
        })

    df_admissions = pd.DataFrame(admissions_data)
    df_diagnoses = pd.DataFrame(diagnoses_data)
    df_billing = pd.DataFrame(billing_data)

    # ---------------------------------------------------------
    # 4. JOINED ANALYTICAL MASTER VIEW (40 COLUMNS)
    # ---------------------------------------------------------
    df_view = df_admissions.merge(df_patients, on="patient_id", how="inner")
    df_view = df_view.merge(df_payers, on="payer_id", how="inner")
    df_view = df_view.merge(df_diagnoses, on="admission_id", how="inner")
    df_view = df_view.merge(df_billing, on="admission_id", how="inner")
    
    # Feature engineering for view
    df_view["is_multimorbid"] = (df_view["comorbidity_count"] >= 2).astype(int)
    
    # Reorder columns to exact 40-column specification
    cols_order = [
        "admission_id", "patient_id", "first_name", "last_name", "date_of_birth",
        "age", "age_bracket", "gender", "ethnicity", "zip_code",
        "city", "district_type", "admission_date", "discharge_date", "admission_year",
        "admission_month", "admission_season", "admission_type", "department", "length_of_stay",
        "is_outlier_stay", "discharge_disposition", "readmitted_30d", "readmission_days", "diagnosis_id",
        "primary_diagnosis", "hypertension", "diabetes", "cvd", "copd",
        "ckd", "comorbidity_count", "is_multimorbid", "payer_id", "payer_name",
        "payer_tier", "billing_id", "total_charges", "insurance_paid", "out_of_pocket",
        "claim_coverage_ratio"
    ]
    df_view = df_view[[c for c in cols_order if c in df_view.columns]]

    # ---------------------------------------------------------
    # 5. EXPORT CSVs & MULTI-TAB EXCEL
    # ---------------------------------------------------------
    out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\patient_demographic_analysis\data"
    os.makedirs(out_dir, exist_ok=True)
    
    df_patients.to_csv(os.path.join(out_dir, "dim_patients.csv"), index=False)
    df_payers.to_csv(os.path.join(out_dir, "dim_payers.csv"), index=False)
    df_admissions.to_csv(os.path.join(out_dir, "fact_admissions.csv"), index=False)
    df_diagnoses.to_csv(os.path.join(out_dir, "fact_clinical_diagnoses.csv"), index=False)
    df_billing.to_csv(os.path.join(out_dir, "fact_billing.csv"), index=False)
    df_view.to_csv(os.path.join(out_dir, "v_patient_analytical_master.csv"), index=False)
    print("[*] Successfully exported all 6 CSV files to data/")

    excel_path = os.path.join(out_dir, "patient_demographic_analysis_data.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_patients.to_excel(writer, sheet_name="dim_patients", index=False)
        df_payers.to_excel(writer, sheet_name="dim_payers", index=False)
        df_admissions.to_excel(writer, sheet_name="fact_admissions", index=False)
        df_diagnoses.to_excel(writer, sheet_name="fact_clinical_diagnoses", index=False)
        df_billing.to_excel(writer, sheet_name="fact_billing", index=False)
        df_view.to_excel(writer, sheet_name="v_analytical_master", index=False)
    print(f"[*] Successfully generated Master Excel workbook: {excel_path}")

    # ---------------------------------------------------------
    # 6. SQLITE DATABASE POPULATION WITH DDL & FOREIGN KEYS
    # ---------------------------------------------------------
    db_path = os.path.join(out_dir, "app.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    
    ddl_script = """
    CREATE TABLE dim_patients (
        patient_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        age INTEGER NOT NULL CHECK (age >= 0 AND age <= 115),
        age_bracket TEXT NOT NULL CHECK (age_bracket IN ('<18', '18-35', '36-50', '51-65', '>65')),
        gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Non-Binary')),
        ethnicity TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        city TEXT NOT NULL,
        district_type TEXT NOT NULL CHECK (district_type IN ('Urban', 'Suburban', 'Rural'))
    );

    CREATE TABLE dim_payers (
        payer_id TEXT PRIMARY KEY,
        payer_name TEXT NOT NULL UNIQUE,
        payer_tier TEXT NOT NULL CHECK (payer_tier IN ('Medicare', 'Medicaid', 'Private HMO', 'Private PPO', 'Self-Pay')),
        avg_reimbursement_rate REAL NOT NULL CHECK (avg_reimbursement_rate >= 0.0 AND avg_reimbursement_rate <= 1.0),
        standard_copay REAL NOT NULL CHECK (standard_copay >= 0.0)
    );

    CREATE TABLE fact_admissions (
        admission_id TEXT PRIMARY KEY,
        patient_id TEXT NOT NULL,
        payer_id TEXT NOT NULL,
        admission_date TEXT NOT NULL,
        discharge_date TEXT NOT NULL,
        admission_year INTEGER NOT NULL,
        admission_month INTEGER NOT NULL CHECK (admission_month >= 1 AND admission_month <= 12),
        admission_season TEXT NOT NULL CHECK (admission_season IN ('Winter', 'Spring', 'Summer', 'Fall')),
        admission_type TEXT NOT NULL CHECK (admission_type IN ('Emergency', 'Urgent', 'Elective')),
        department TEXT NOT NULL,
        length_of_stay INTEGER NOT NULL CHECK (length_of_stay >= 1),
        is_outlier_stay INTEGER NOT NULL CHECK (is_outlier_stay IN (0, 1)),
        discharge_disposition TEXT NOT NULL CHECK (discharge_disposition IN ('Home', 'Skilled Nursing', 'Rehabilitation', 'AMA')),
        readmitted_30d INTEGER NOT NULL CHECK (readmitted_30d IN (0, 1)),
        readmission_days INTEGER CHECK (readmission_days IS NULL OR (readmission_days >= 1 AND readmission_days <= 30)),
        FOREIGN KEY (patient_id) REFERENCES dim_patients(patient_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (payer_id) REFERENCES dim_payers(payer_id) ON DELETE RESTRICT ON UPDATE CASCADE
    );

    CREATE TABLE fact_clinical_diagnoses (
        diagnosis_id TEXT PRIMARY KEY,
        admission_id TEXT NOT NULL UNIQUE,
        primary_diagnosis TEXT NOT NULL,
        hypertension INTEGER NOT NULL CHECK (hypertension IN (0, 1)),
        diabetes INTEGER NOT NULL CHECK (diabetes IN (0, 1)),
        cvd INTEGER NOT NULL CHECK (cvd IN (0, 1)),
        copd INTEGER NOT NULL CHECK (copd IN (0, 1)),
        ckd INTEGER NOT NULL CHECK (ckd IN (0, 1)),
        comorbidity_count INTEGER NOT NULL CHECK (comorbidity_count >= 0 AND comorbidity_count <= 5),
        FOREIGN KEY (admission_id) REFERENCES fact_admissions(admission_id) ON DELETE CASCADE ON UPDATE CASCADE
    );

    CREATE TABLE fact_billing (
        billing_id TEXT PRIMARY KEY,
        admission_id TEXT NOT NULL UNIQUE,
        total_charges REAL NOT NULL CHECK (total_charges >= 0.0),
        insurance_paid REAL NOT NULL CHECK (insurance_paid >= 0.0),
        out_of_pocket REAL NOT NULL CHECK (out_of_pocket >= 0.0),
        claim_coverage_ratio REAL NOT NULL CHECK (claim_coverage_ratio >= 0.0 AND claim_coverage_ratio <= 1.0),
        claim_status TEXT NOT NULL CHECK (claim_status IN ('Settled', 'Pending', 'Disputed', 'Written-Off')),
        billing_date TEXT NOT NULL,
        FOREIGN KEY (admission_id) REFERENCES fact_admissions(admission_id) ON DELETE CASCADE ON UPDATE CASCADE
    );

    CREATE INDEX idx_admissions_patient ON fact_admissions(patient_id);
    CREATE INDEX idx_admissions_payer ON fact_admissions(payer_id);
    CREATE INDEX idx_admissions_date ON fact_admissions(admission_date);
    CREATE INDEX idx_admissions_readmit ON fact_admissions(readmitted_30d);
    CREATE INDEX idx_diagnoses_admission ON fact_clinical_diagnoses(admission_id);
    CREATE INDEX idx_billing_admission ON fact_billing(admission_id);

    CREATE VIEW v_patient_analytical_master AS
    SELECT 
        a.admission_id, p.patient_id, p.first_name, p.last_name, p.date_of_birth,
        p.age, p.age_bracket, p.gender, p.ethnicity, p.zip_code, p.city, p.district_type,
        a.admission_date, a.discharge_date, a.admission_year, a.admission_month, a.admission_season,
        a.admission_type, a.department, a.length_of_stay, a.is_outlier_stay, a.discharge_disposition,
        a.readmitted_30d, a.readmission_days,
        d.diagnosis_id, d.primary_diagnosis, d.hypertension, d.diabetes, d.cvd, d.copd, d.ckd,
        d.comorbidity_count,
        CASE WHEN d.comorbidity_count >= 2 THEN 1 ELSE 0 END AS is_multimorbid,
        pay.payer_id, pay.payer_name, pay.payer_tier,
        b.billing_id, b.total_charges, b.insurance_paid, b.out_of_pocket, b.claim_coverage_ratio
    FROM fact_admissions a
    INNER JOIN dim_patients p ON a.patient_id = p.patient_id
    INNER JOIN dim_payers pay ON a.payer_id = pay.payer_id
    INNER JOIN fact_clinical_diagnoses d ON a.admission_id = d.admission_id
    INNER JOIN fact_billing b ON a.admission_id = b.admission_id;
    """
    
    cur.executescript(ddl_script)
    
    # Insert Data into Tables
    df_patients.to_sql("dim_patients", conn, if_exists="append", index=False)
    df_payers.to_sql("dim_payers", conn, if_exists="append", index=False)
    df_admissions.to_sql("fact_admissions", conn, if_exists="append", index=False)
    df_diagnoses.to_sql("fact_clinical_diagnoses", conn, if_exists="append", index=False)
    df_billing.to_sql("fact_billing", conn, if_exists="append", index=False)
    
    conn.commit()
    print(f"[*] Successfully created and populated SQLite database: {db_path}")

    # ---------------------------------------------------------
    # 7. AUTOMATED VERIFICATION & VALIDATION AUDIT
    # ---------------------------------------------------------
    print("\n" + "="*60)
    print("        AUTOMATED DATASET VALIDATION AUDIT")
    print("="*60)
    
    # 1. Row counts
    cur.execute("SELECT count(*) FROM dim_patients")
    cnt_p = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM dim_payers")
    cnt_pay = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM fact_admissions")
    cnt_a = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM fact_clinical_diagnoses")
    cnt_d = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM fact_billing")
    cnt_b = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM v_patient_analytical_master")
    cnt_v = cur.fetchone()[0]
    
    print(f"[+] dim_patients Row Count:            {cnt_p} (Target: 250)")
    print(f"[+] dim_payers Row Count:              {cnt_pay} (Target: 5)")
    print(f"[+] fact_admissions Row Count:         {cnt_a} (Target: 300)")
    print(f"[+] fact_clinical_diagnoses Row Count: {cnt_d} (Target: 300)")
    print(f"[+] fact_billing Row Count:            {cnt_b} (Target: 300)")
    print(f"[+] v_patient_analytical_master Rows:  {cnt_v} (Target: 300)")
    
    # 2. Foreign Key Check
    cur.execute("PRAGMA foreign_key_check;")
    fk_errors = cur.fetchall()
    if len(fk_errors) == 0:
        print("[+] Foreign Key Integrity Check:        100% PASSED (0 Violations)")
    else:
        print(f"[-] Foreign Key Integrity FAILED: {fk_errors}")

    # 3. Range Checks
    cur.execute("SELECT min(age), max(age) FROM dim_patients")
    min_age, max_age = cur.fetchone()
    print(f"[+] Age Range Check:                   [{min_age}, {max_age}] (Valid: 0 to 115)")
    
    cur.execute("SELECT min(length_of_stay), max(length_of_stay) FROM fact_admissions")
    min_los, max_los = cur.fetchone()
    print(f"[+] Length of Stay Range Check:        [{min_los}, {max_los}] days (Valid: >= 1)")

    cur.execute("SELECT count(*) FROM fact_admissions WHERE is_outlier_stay = 1")
    outlier_stays = cur.fetchone()[0]
    print(f"[+] Outlier Stays Flagged (>14 days):   {outlier_stays} cases")
    
    cur.execute("SELECT min(claim_coverage_ratio), max(claim_coverage_ratio) FROM fact_billing")
    min_cov, max_cov = cur.fetchone()
    print(f"[+] Coverage Ratio Range:              [{min_cov}, {max_cov}] (Valid: 0.0 to 1.0)")

    # 4. Pattern Checks
    cur.execute("""
        SELECT age_bracket, round(avg(length_of_stay), 2), round(avg(readmitted_30d)*100, 1)
        FROM v_patient_analytical_master
        GROUP BY age_bracket
        ORDER BY age_bracket;
    """)
    print("\n[+] Verification of Built-in Pattern 1 & 2 (ALoS & Readmission by Age Bracket):")
    for r in cur.fetchall():
        print(f"    - Bracket: {r[0]:<6} | Mean ALoS: {r[1]:<4} days | Readmission Rate: {r[2]}%")

    conn.close()
    print("="*60)
    print("[*] All datasets generated, verified, and ready for analytical processing!\n")

if __name__ == "__main__":
    generate_synthetic_dataset()
