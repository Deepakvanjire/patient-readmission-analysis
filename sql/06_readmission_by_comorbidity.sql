-- ============================================================
-- 06_readmission_by_comorbidity.sql
-- Readmission Rate by Comorbidity Count and Charlson Index
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission rate by comorbidity_count
SELECT
    p.comorbidity_count,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.comorbidity_count
ORDER BY p.comorbidity_count;

-- B. Readmission rate by charlson_index bucket
SELECT
    CASE
        WHEN a.charlson_index = 0             THEN '0 - Low'
        WHEN a.charlson_index BETWEEN 1 AND 2 THEN '1-2 - Moderate'
        WHEN a.charlson_index BETWEEN 3 AND 5 THEN '3-5 - High'
        WHEN a.charlson_index > 5             THEN '6+ - Very High'
    END                                           AS charlson_bucket,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days,
    ROUND(AVG(p.comorbidity_count), 2)            AS avg_comorbidities
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY charlson_bucket
ORDER BY
    FIELD(charlson_bucket, '0 - Low', '1-2 - Moderate', '3-5 - High', '6+ - Very High');

-- C. Comorbidity x charlson cross-tab summary
SELECT
    p.comorbidity_count,
    ROUND(AVG(a.charlson_index), 2)               AS avg_charlson,
    COUNT(a.admission_id)                         AS total_admissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.comorbidity_count
ORDER BY p.comorbidity_count;

-- D. Clinical lab values vs readmission
SELECT
    readmitted_30d,
    ROUND(AVG(hba1c), 2)                          AS avg_hba1c,
    ROUND(AVG(creatinine), 2)                     AS avg_creatinine,
    ROUND(AVG(haemoglobin), 2)                    AS avg_haemoglobin,
    ROUND(AVG(systolic_bp), 2)                    AS avg_systolic_bp,
    ROUND(AVG(charlson_index), 2)                 AS avg_charlson
FROM admissions
GROUP BY readmitted_30d;
