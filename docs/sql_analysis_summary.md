# SQL Analysis Summary
## Patient Readmission Analysis — Synthetic Indian Hospital Data

> **DISCLAIMER:** All findings are from synthetic data for portfolio purposes only.

---

## Query File Overview

| File | Topic | Key Metric |
|---|---|---|
| `01_overall_readmission.sql` | Overall rate + year/month trend | Baseline rate ~11.84% |
| `02_readmission_by_diagnosis.sql` | By diagnosis category and ICD-10 code | Highest-rate diagnosis categories |
| `03_readmission_by_age.sql` | By age group and gender | Older groups expected higher |
| `04_readmission_by_insurance.sql` | By insurance type and BPL card | Insurance-type rate comparison |
| `05_readmission_by_previous_admissions.sql` | By prior hospitalization history | Rate increases with history |
| `06_readmission_by_comorbidity.sql` | By comorbidity count and Charlson index | Rate increases with burden |
| `07_readmission_by_hospital.sql` | By hospital, tier, teaching status | Hospital-level benchmarks |
| `08_readmission_by_state.sql` | By patient home state and hospital state | State-level comparisons |
| `09_readmission_by_ward.sql` | By ward type and ward×discharge interaction | ICU vs General comparison |
| `10_readmission_by_admission_type.sql` | By admission type and discharge type | Emergency and LAMA patterns |
| `11_readmission_financial_impact.sql` | Financial burden of readmissions | Cost differential |
| `12_followup_prioritization.sql` | Follow-up priority scoring and tier summary | HIGH/MEDIUM/LOW segmentation |

---

## Key SQL Patterns Used

### Basic Rate Calculation
```sql
SELECT
    dimension_column,
    COUNT(admission_id)                  AS total_admissions,
    SUM(readmitted_30d)                  AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)  AS readmission_rate_pct
FROM admissions
GROUP BY dimension_column
ORDER BY readmission_rate_pct DESC;
```

### Cross-Table Join Pattern
```sql
SELECT
    p.insurance_type,
    COUNT(a.admission_id)               AS total_admissions,
    ROUND(AVG(a.readmitted_30d)*100, 2) AS readmission_rate_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.insurance_type;
```

### Age Group Bucketing
```sql
CASE
    WHEN p.age BETWEEN 18 AND 29 THEN '18-29'
    WHEN p.age BETWEEN 30 AND 44 THEN '30-44'
    WHEN p.age BETWEEN 45 AND 59 THEN '45-59'
    WHEN p.age BETWEEN 60 AND 74 THEN '60-74'
    WHEN p.age >= 75             THEN '75+'
END AS age_group
```

### Primary Diagnosis Join (rank = 1)
```sql
FROM admissions a
JOIN diagnoses d
    ON a.admission_id = d.admission_id
    AND d.diag_rank = 1
```

---

## Expected Findings (from synthetic dataset)

| Dimension | Expected Pattern |
|---|---|
| Age group 75+ | Higher readmission rate than 18-29 |
| Charlson ≥ 3 | Higher readmission than Charlson 0 |
| prev_admissions 6+ | Higher than patients with 0 |
| Emergency admissions | Higher than Elective |
| LAMA discharge | Highest among discharge types |
| ICU ward | Higher than General ward |
| High cost admissions | Higher readmission rate |
| HIGH priority tier | Higher actual readmission rate than MEDIUM/LOW |

---

## Running the SQL Files

```sql
-- In MySQL Workbench or CLI:
SOURCE sql/01_overall_readmission.sql;
SOURCE sql/02_readmission_by_diagnosis.sql;
-- ... etc.
```

Or run all at once:
```bash
mysql -u root -p patient_readmission < sql/01_overall_readmission.sql
```
