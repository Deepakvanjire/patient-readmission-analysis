-- ============================================================
-- 02_readmission_by_diagnosis.sql
-- Readmission Rate by Diagnosis Category
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission rate per diagnosis category (primary diagnosis only)
SELECT
    d.diag_category,
    COUNT(DISTINCT a.admission_id)                AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN diagnoses d
    ON a.admission_id = d.admission_id
    AND d.diag_rank = 1
GROUP BY d.diag_category
ORDER BY readmission_rate_pct DESC;

-- B. Top 10 ICD-10 codes by readmission count
SELECT
    d.icd10_code,
    d.diag_desc,
    d.diag_category,
    COUNT(DISTINCT a.admission_id)                AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN diagnoses d
    ON a.admission_id = d.admission_id
    AND d.diag_rank = 1
GROUP BY d.icd10_code, d.diag_desc, d.diag_category
HAVING total_admissions >= 100
ORDER BY readmissions DESC
LIMIT 10;

-- C. Top 10 diagnosis categories by volume
SELECT
    d.diag_category,
    COUNT(DISTINCT a.admission_id)                AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days,
    ROUND(AVG(a.charlson_index), 2)               AS avg_charlson
FROM admissions a
JOIN diagnoses d
    ON a.admission_id = d.admission_id
    AND d.diag_rank = 1
GROUP BY d.diag_category
ORDER BY total_admissions DESC
LIMIT 10;
