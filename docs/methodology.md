# Methodology
## Patient Readmission Analysis — Synthetic Indian Hospital Data

> **DISCLAIMER:** This project uses synthetic hospital data for analytical and portfolio purposes.
> All findings should not be interpreted as clinical guidance or validated medical models.

---

## 1. Project Overview

This project performs end-to-end data analytics on a synthetic Indian hospital dataset containing 86,400 patients, 120,000 admissions, 271,341 diagnoses, 33 hospitals, and 120,000 billing records.

The primary analytical goal is to identify historical patterns in 30-day hospital readmissions and construct a transparent, data-derived follow-up priority segmentation.

---

## 2. Data Generation

The dataset is **fully synthetic** and was designed to represent realistic Indian hospital scenarios including:
- Multi-state patient distribution across Indian states
- Indian health insurance scheme types (Ayushman Bharat, ESI, Private)
- BPL (Below Poverty Line) card holders
- Typical comorbidity patterns (diabetes, hypertension, CKD, COPD)
- ICD-10 coded diagnoses with category groupings

No real patient data was used at any stage.

---

## 3. Data Pipeline

```
Raw CSVs (raw_data/)
        ↓
Python Cleaning (python/clean_data.py)
        ↓
Cleaned CSVs (cleaned_data/)
        ↓
MySQL Import (python/import_to_mysql.py)
        ↓
MySQL Database (patient_readmission)
        ↓
SQL Analysis (sql/*.sql)
        ↓
Python Analysis & Charts (python/analyze_data.py)
        ↓
Power BI Dashboard (powerbi/)
```

---

## 4. Data Cleaning Steps

1. **Column standardization:** All column names stripped, lowercased, and spaces replaced with underscores.
2. **Duplicate removal:** Exact duplicate rows removed from all tables.
3. **ID preservation:** All ID columns (`patient_id`, `admission_id`, etc.) kept as strings (UUID format). Never converted to integers.
4. **Missing values:**
   - `insurance_type` nulls → replaced with `"Unknown"` (transparent, documented category)
   - No other columns had missing values
5. **Type enforcement:** Numeric columns parsed with `pd.to_numeric(errors="coerce")`. Date columns parsed with `pd.to_datetime(errors="coerce")`.
6. **Relationship validation:** Checked all FK references in Python before loading to MySQL.

---

## 5. Readmission Target Variable

`readmitted_30d` is a binary flag (0/1) embedded in the synthetic admissions dataset.

- `1` = This admission was followed by another recorded admission for the same patient within 30 days in the synthetic dataset.
- `0` = No subsequent admission recorded within 30 days.

**This is a historical dataset flag, not a real-time clinical prediction.**

---

## 6. Historical Follow-Up Priority — Scoring Methodology

### Purpose
Identify admissions that, based on historical data patterns, share characteristics commonly associated with higher readmission rates in the dataset.

### Variable Selection
Variables were selected based on:
1. Clinical relevance documented in readmission literature (for realistic scenario design)
2. Availability in the synthetic dataset
3. Measurable contribution to readmission patterns observed in the data

### Scoring Table

| Factor | Condition | Points | Rationale |
|---|---|---|---|
| Previous admissions | ≥ 3 | +3 | Patients with frequent prior hospitalizations show higher readmission patterns |
| Comorbidity count | ≥ 3 | +3 | Multiple comorbidities increase clinical complexity |
| Charlson index | ≥ 3 | +3 | Higher disease burden associated with higher readmission in dataset |
| Age | ≥ 60 | +2 | Older patients more vulnerable |
| Length of stay | ≥ 7 days | +2 | Longer stays indicate more complex conditions |
| Admission type | Emergency | +2 | Emergency admissions reflect acute severity |
| Discharge type | LAMA | +3 | Left Against Medical Advice — highest readmission risk in dataset |
| Discharge type | Referred | +2 | Referred patients indicate unresolved conditions |
| Ward type | ICU | +2 | ICU admissions reflect critical illness |

### Priority Tiers

| Total Score | Label | Interpretation |
|---|---|---|
| 0–4 | LOW | Historically lower readmission pattern |
| 5–9 | MEDIUM | Historically moderate readmission pattern |
| 10+ | HIGH | Historically higher readmission pattern |

### Important Limitations
- Scores are fixed, equal-weight (within categories) — no statistical weight optimization
- Thresholds (≥3, ≥60, ≥7) are chosen for interpretability, not derived from regression coefficients
- This is a **rule-based descriptive segmentation**, not a predictive model
- Scores do not account for interactions between variables
- The model has not been validated on external or real-world data

---

## 7. SQL Analysis Approach

All 12 SQL queries use:
- Simple aggregations (`COUNT`, `SUM`, `AVG`)
- `GROUP BY` with relevant dimensions
- `ROUND` for readability
- Filtered to minimum admission volumes where applicable (to avoid noise from tiny groups)
- No window functions beyond simple `OVER()` for percentages

---

## 8. Python Analysis Approach

- Library: `pandas`, `numpy`, `matplotlib`
- All charts use a consistent professional colour palette
- Readmission rates colour-coded: blue (below average), red (above average)
- Follow-up priority uses: green (LOW), amber (MEDIUM), red (HIGH)
- All charts saved to `python/output/` at 150 DPI

---

## 9. Optional Machine Learning (Logistic Regression)

If pursued:
- **Target:** `readmitted_30d`
- **Features:** `age`, `comorbidity_count`, `prev_admissions`, `los_days`, `num_procedures`, `charlson_index`, `hba1c`, `creatinine`, `haemoglobin`, `systolic_bp` + encoded categoricals
- **Model:** Logistic Regression (primary), Random Forest (optional comparison)
- **Evaluation:** Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix
- **Class imbalance handling:** Class weights or SMOTE if needed (readmission rate ~11.84%)
- **Disclaimer:** Analytical experiment on synthetic data only

---

## 10. Power BI Model

Star schema:
- **FACT tables:** admissions, billing, diagnoses
- **DIM tables:** patients, hospitals
- Relationships are single-directional (DIM → FACT), except diagnoses which uses bidirectional filtering to allow diagnosis category slicing.
