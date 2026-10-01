# Patient Readmission Analysis & Hospital Follow-Up Intelligence System

> **⚠️ DISCLAIMER:** This project uses **synthetic** Indian hospital data generated for analytical and portfolio purposes only. All findings, patterns, and follow-up prioritizations reflect historical patterns in this synthetic dataset and should **not** be interpreted as clinical diagnosis, medical advice, or a validated clinical prediction model.

---

## 📋 Business Problem

Hospital readmissions within 30 days of discharge are a key quality and cost indicator in healthcare management. This project addresses the question:

> **"Which patient profiles have the highest historical 30-day readmission rates, and which profiles should the hospital consider for intensive post-discharge follow-up based on historical data?"**

---

## 📁 Project Structure

```
Patient readmission project/
│
├── raw_data/                    # Original synthetic CSVs
│   ├── admissions.csv
│   ├── billing.csv
│   ├── diagnoses.csv
│   ├── hospitals.csv
│   └── patients.csv
│
├── cleaned_data/                # Cleaned and validated CSVs
│   ├── admissions_clean.csv
│   ├── billing_clean.csv
│   ├── diagnoses_clean.csv
│   ├── hospitals_clean.csv
│   └── patients_clean.csv
│
├── python/
│   ├── clean_data.py            # Data cleaning and validation
│   ├── import_to_mysql.py       # Automated MySQL import (chunked)
│   ├── validate_database.py     # Post-import database validation
│   ├── analyze_data.py          # EDA + charts + follow-up priority
│   └── output/                  # Generated charts (PNG)
│
├── sql/
│   ├── 01_overall_readmission.sql
│   ├── 02_readmission_by_diagnosis.sql
│   ├── 03_readmission_by_age.sql
│   ├── 04_readmission_by_insurance.sql
│   ├── 05_readmission_by_previous_admissions.sql
│   ├── 06_readmission_by_comorbidity.sql
│   ├── 07_readmission_by_hospital.sql
│   ├── 08_readmission_by_state.sql
│   ├── 09_readmission_by_ward.sql
│   ├── 10_readmission_by_admission_type.sql
│   ├── 11_readmission_financial_impact.sql
│   └── 12_followup_prioritization.sql
│
├── docs/
│   ├── data_dictionary.md
│   ├── data_quality_report.md
│   ├── business_questions.md
│   ├── sql_analysis_summary.md
│   ├── methodology.md
│   ├── powerbi_dashboard_guide.md
│   └── limitations.md
│
├── powerbi/
│   ├── DAX_Measures.txt
│   └── dashboard_guide.md
│
├── .env.example                 # Environment variables template
├── .gitignore
└── README.md
```

---

## 🗄️ Dataset

| Table | Rows | Description |
|---|---|---|
| patients | 86,400 | Patient demographics and insurance |
| admissions | 120,000 | Hospital admissions with clinical data |
| diagnoses | 271,341 | ICD-10 coded diagnoses per admission |
| hospitals | 33 | Hospital metadata (tier, state, teaching) |
| billing | 120,000 | Cost and subsidy information per admission |

**Overall 30-day readmission rate: ~11.84%**

---

## 🏗️ Data Architecture

```
                    PATIENTS (DIM)
                    patient_id PK
                         │
                    ADMISSIONS (FACT — central)
                 admission_id PK
                 patient_id FK ──────────────┘
                 hospital_id FK ─────────────┐
                    /       \                │
             DIAGNOSES     BILLING      HOSPITALS (DIM)
             (FACT)        (FACT)       hospital_id PK
             admission_id FK  admission_id FK
```

---

## ⚙️ How to Run

### 1. Environment Setup

```bash
pip install pandas numpy matplotlib mysql-connector-python python-dotenv scikit-learn seaborn
```

Copy `.env.example` to `.env` and fill in your MySQL credentials:

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=patient_readmission
```

### 2. Data Cleaning

```bash
python python/clean_data.py
```

### 3. MySQL Import

Ensure the `patient_readmission` database and its 5 tables exist in MySQL, then:

```bash
python python/import_to_mysql.py
```

Expected output: 597,773 total records imported across 5 tables.

### 4. Database Validation

```bash
python python/validate_database.py
```

### 5. SQL Analysis

Open any `.sql` file in MySQL Workbench and run against `patient_readmission`, or:

```bash
mysql -u root -p patient_readmission < sql/01_overall_readmission.sql
```

### 6. Python Analysis & Charts

```bash
python python/analyze_data.py
```

Charts saved to `python/output/`.

### 7. Power BI Dashboard

See `powerbi/dashboard_guide.md` for full connection and setup instructions.

---

## 📊 Key Findings (Synthetic Dataset)

| Business Question | Finding |
|---|---|
| Overall 30-day readmission rate | ~11.84% |
| Age-group pattern | Older age groups show elevated historical readmission rates |
| Comorbidity impact | Readmission rises with comorbidity count |
| Charlson index impact | Charlson ≥ 3 linked to higher rates |
| Prior admissions impact | 6+ prior admissions: highest readmission |
| Discharge type | LAMA discharges: highest readmission rates |
| Financial impact | Readmitted patients have higher average cost |
| Historical follow-up priority distribution | High: ~5.5%, Medium: ~59.1%, Low: ~35.5% |

---

## 🎯 Historical Follow-Up Priority

The project includes a transparent, data-derived **Historical Follow-Up Priority** segmentation (LOW / MEDIUM / HIGH).

| Tier | Score | Description |
|---|---|---|
| LOW | 0–4 | Historically lower readmission pattern |
| MEDIUM | 5–9 | Historically moderate readmission pattern |
| HIGH | 10+ | Historically higher readmission pattern |

Factors scored: previous admissions, comorbidity count, Charlson index, age ≥ 60, LOS ≥ 7 days, Emergency admission, LAMA discharge, Referred discharge, ICU ward.

**This is NOT a clinical diagnosis or prediction model.**

---

## 🧠 Optional Machine Learning

An optional logistic regression model can be trained:
- **Target:** `readmitted_30d`
- **Features:** `age`, `comorbidity_count`, `prev_admissions`, `los_days`, `charlson_index`, clinical lab values, encoded categoricals
- **Evaluation:** Accuracy, Precision, Recall, F1, ROC-AUC

This is an analytical experiment on synthetic data only.

---

## 🔧 Technologies Used

| Category | Technology |
|---|---|
| Programming | Python 3.9 |
| Data Manipulation | Pandas, NumPy |
| Visualisation | Matplotlib |
| Database | MySQL 8.0 |
| Query Language | SQL |
| BI Dashboard | Power BI Desktop |
| BI Expressions | DAX |
| ML (Optional) | Scikit-learn |
| Environment | python-dotenv |

---

## 📚 Documentation

| File | Contents |
|---|---|
| `docs/data_dictionary.md` | Column definitions for all 5 tables |
| `docs/data_quality_report.md` | Row counts, duplicates, nulls, FK checks |
| `docs/business_questions.md` | 13 business questions with SQL references |
| `docs/methodology.md` | Data pipeline, scoring logic, approach |
| `docs/sql_analysis_summary.md` | SQL file guide and expected findings |
| `docs/powerbi_dashboard_guide.md` | Power BI setup and measure reference |
| `docs/limitations.md` | Data, model, and interpretation limitations |

---

## ⚠️ Limitations

- All data is **synthetic** — results do not reflect real hospital performance
- The follow-up priority segmentation is **descriptive**, not a clinical prediction model
- Hospital comparisons are **unadjusted** for patient case mix
- Associations observed are **correlational**, not causal

See `docs/limitations.md` for the full limitations statement.

---

## 👤 Portfolio

This project demonstrates:
- ✅ Python data engineering (ETL pipeline)
- ✅ SQL analytical queries (12 analysis files)
- ✅ Relational database design (MySQL star schema)
- ✅ Data cleaning and validation
- ✅ Exploratory data analysis
- ✅ Business insight generation
- ✅ Power BI dashboard design (DAX measures)
- ✅ Documentation and methodology transparency
