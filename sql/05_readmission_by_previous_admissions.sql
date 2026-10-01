-- ============================================================
-- 05_readmission_by_previous_admissions.sql
-- Readmission Rate by Previous Admissions Count
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission rate grouped by prev_admissions bucket
SELECT
    CASE
        WHEN p.prev_admissions = 0 THEN '0 (First visit)'
        WHEN p.prev_admissions = 1 THEN '1'
        WHEN p.prev_admissions = 2 THEN '2'
        WHEN p.prev_admissions BETWEEN 3 AND 5 THEN '3-5'
        WHEN p.prev_admissions > 5             THEN '6+'
        ELSE 'Unknown'
    END                                           AS prev_admissions_group,
    p.prev_admissions,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY prev_admissions_group, p.prev_admissions
ORDER BY p.prev_admissions;

-- B. Readmission rate by bucketed groups (for dashboard)
SELECT
    CASE
        WHEN p.prev_admissions = 0             THEN '0 - First Visit'
        WHEN p.prev_admissions BETWEEN 1 AND 2 THEN '1-2 Previous'
        WHEN p.prev_admissions BETWEEN 3 AND 5 THEN '3-5 Previous'
        WHEN p.prev_admissions > 5             THEN '6+ Previous'
    END                                           AS prev_admissions_bucket,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY prev_admissions_bucket
ORDER BY readmission_rate_pct DESC;

-- C. Distribution of prev_admissions across all patients
SELECT
    prev_admissions,
    COUNT(*)                                      AS patient_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_patients
FROM patients
GROUP BY prev_admissions
ORDER BY prev_admissions;
