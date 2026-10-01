-- ============================================================
-- 04_readmission_by_insurance.sql
-- Readmission Rate by Insurance Type
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission rate by insurance type
SELECT
    p.insurance_type,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days,
    ROUND(AVG(a.charlson_index), 2)               AS avg_charlson_index,
    ROUND(AVG(p.comorbidity_count), 2)            AS avg_comorbidities
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.insurance_type
ORDER BY readmission_rate_pct DESC;

-- B. Insurance x BPL card cross-analysis
SELECT
    p.insurance_type,
    p.bpl_card,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.insurance_type, p.bpl_card
ORDER BY p.insurance_type, p.bpl_card;

-- C. Insurance patient count and distribution
SELECT
    insurance_type,
    COUNT(*)                                      AS patient_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_total
FROM patients
GROUP BY insurance_type
ORDER BY patient_count DESC;
