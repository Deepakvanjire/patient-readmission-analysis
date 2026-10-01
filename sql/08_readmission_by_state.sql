-- ============================================================
-- 08_readmission_by_state.sql
-- Readmission Rate by State
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission rate by patient home state
SELECT
    p.state,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days,
    ROUND(AVG(p.comorbidity_count), 2)            AS avg_comorbidities
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.state
ORDER BY readmission_rate_pct DESC;

-- B. Readmission rate by hospital location state
SELECT
    h.state                                       AS hospital_state,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    COUNT(DISTINCT h.hospital_id)                 AS hospitals_in_state
FROM admissions a
JOIN hospitals h ON a.hospital_id = h.hospital_id
GROUP BY h.state
ORDER BY readmission_rate_pct DESC;

-- C. State with most admissions (top 10)
SELECT
    p.state,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.state
ORDER BY total_admissions DESC
LIMIT 10;
