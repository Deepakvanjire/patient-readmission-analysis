# Data Dictionary
## Patient Readmission Analysis — Synthetic Indian Hospital Data

> **DISCLAIMER:** All data is synthetic and generated for portfolio/analytical purposes only.

---

## Table: patients

| Column | Type | Description |
|---|---|---|
| `patient_id` | VARCHAR (UUID) | Unique patient identifier. Primary key. Stored as string — do not convert to numeric. |
| `age` | INTEGER | Patient age in years at time of data generation. Range: 18–100. |
| `gender` | VARCHAR | Patient gender. Values: `M`, `F`. |
| `state` | VARCHAR | Patient's home state (Indian state name). |
| `bpl_card` | VARCHAR | Below Poverty Line card holder indicator. Values: `True`, `False`. |
| `insurance_type` | VARCHAR | Patient's primary health insurance type. Values: `Ayushman`, `ESI`, `Private`, `Unknown`. `Unknown` represents records where insurance was not recorded. |
| `comorbidity_count` | INTEGER | Number of documented comorbid conditions for the patient. Range: 0–6. |
| `prev_admissions` | INTEGER | Number of hospital admissions prior to those recorded in this dataset. Range: 0–10. |

---

## Table: admissions

| Column | Type | Description |
|---|---|---|
| `admission_id` | VARCHAR (UUID) | Unique admission identifier. Primary key. |
| `patient_id` | VARCHAR (UUID) | Foreign key → `patients.patient_id`. |
| `admit_date` | DATE | Date the patient was admitted (YYYY-MM-DD). |
| `discharge_date` | DATE | Date the patient was discharged (YYYY-MM-DD). Must be ≥ admit_date. |
| `los_days` | INTEGER | Length of stay in days (discharge_date − admit_date). |
| `admit_type` | VARCHAR | Type of admission. Values: `Emergency`, `Elective`, `OPD`, `Trauma`. |
| `ward_type` | VARCHAR | Type of ward the patient was admitted to. Values: `General`, `ICU`, `Private`, `Semi-Private`. |
| `hospital_id` | VARCHAR (UUID) | Foreign key → `hospitals.hospital_id`. |
| `discharge_type` | VARCHAR | How the patient was discharged. Values: `Recovered`, `LAMA` (Left Against Medical Advice), `Referred`, `Expired`. |
| `num_procedures` | INTEGER | Number of clinical procedures performed during the admission. |
| `charlson_index` | INTEGER | Charlson Comorbidity Index score — a synthetic approximation of patient disease burden. Higher values indicate more severe comorbidity burden in this dataset. |
| `hba1c` | FLOAT | Glycated haemoglobin value (%). Indicator of blood glucose control (synthetic). |
| `creatinine` | FLOAT | Serum creatinine level (mg/dL). Indicator of kidney function (synthetic). |
| `haemoglobin` | FLOAT | Haemoglobin level (g/dL). Indicator of anaemia status (synthetic). |
| `systolic_bp` | INTEGER | Systolic blood pressure (mmHg) (synthetic). |
| `readmitted_30d` | INTEGER (0/1) | Target indicator: 1 if the patient has a subsequent recorded admission within 30 days in the synthetic dataset; 0 otherwise. **Not a clinical diagnosis.** |
| `readmitted_7d` | INTEGER (0/1) | Indicator: 1 if the patient has a subsequent recorded admission within 7 days in the synthetic dataset; 0 otherwise. |

---

## Table: diagnoses

| Column | Type | Description |
|---|---|---|
| `diag_id` | VARCHAR (UUID) | Unique diagnosis record identifier. Primary key. |
| `admission_id` | VARCHAR (UUID) | Foreign key → `admissions.admission_id`. One admission may have multiple diagnosis rows. |
| `icd10_code` | VARCHAR | ICD-10 diagnosis code (synthetic approximation). |
| `diag_desc` | VARCHAR | Plain-language description of the ICD-10 code. |
| `diag_rank` | INTEGER | Rank/order of diagnosis for this admission. `1` = primary diagnosis; higher values = secondary/tertiary diagnoses. |
| `diag_category` | VARCHAR | Grouped diagnostic category (e.g., Cardiovascular, Respiratory, Endocrine). Derived from ICD-10 chapter. |

---

## Table: hospitals

| Column | Type | Description |
|---|---|---|
| `hospital_id` | VARCHAR (UUID) | Unique hospital identifier. Primary key. |
| `name` | VARCHAR | Hospital name (synthetic). |
| `state` | VARCHAR | Indian state where the hospital is located. |
| `tier` | VARCHAR | Hospital tier classification. Values: `Tier 1`, `Tier 2`, `Tier 3`. Tier 1 = large urban; Tier 3 = smaller/rural. |
| `beds` | INTEGER | Number of hospital beds. |
| `teaching` | VARCHAR | Whether the hospital is a teaching/academic hospital. Values: `Yes`, `No`. |

---

## Table: billing

| Column | Type | Description |
|---|---|---|
| `bill_id` | VARCHAR (UUID) | Unique billing record identifier. Primary key. |
| `admission_id` | VARCHAR (UUID) | Foreign key → `admissions.admission_id`. One-to-one relationship. |
| `total_cost_inr` | FLOAT | Total cost of the admission in Indian Rupees (INR) (synthetic). |
| `govt_subsidy_inr` | FLOAT | Government subsidy applied (INR) (synthetic). |
| `out_of_pocket_inr` | FLOAT | Patient's out-of-pocket cost after subsidy (INR) (synthetic). |
| `cost_category` | VARCHAR | Cost tier classification. Values: `Low`, `Medium`, `High`, `Very High`. |

---

## Key Derived Metrics (computed in analysis)

| Metric | Formula | Description |
|---|---|---|
| Readmission Rate | `SUM(readmitted_30d) / COUNT(admission_id)` | Proportion of admissions followed by readmission within 30 days |
| Age Group | Binned from `age` | 18-29, 30-44, 45-59, 60-74, 75+ |
| Charlson Bucket | Binned from `charlson_index` | 0, 1-2, 3-5, 6+ |
| Priority Score | Sum of weighted dataset factors | See `12_followup_prioritization.sql` and `methodology.md` |
| Historical Follow-Up Priority | Tiered from priority score | LOW (0-4), MEDIUM (5-9), HIGH (10+) |
