-- ============================================================
-- 07_readmission_by_hospital.sql
-- Readmission Rate by Hospital
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission rate per hospital (with tier and teaching info)
SELECT
    h.hospital_id,
    h.name                                        AS hospital_name,
    h.state                                       AS hospital_state,
    h.tier,
    h.teaching,
    h.beds,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days
FROM admissions a
JOIN hospitals h ON a.hospital_id = h.hospital_id
GROUP BY h.hospital_id, h.name, h.state, h.tier, h.teaching, h.beds
ORDER BY readmission_rate_pct DESC;

-- B. Top 10 hospitals by readmission rate (min 500 admissions)
SELECT
    h.name                                        AS hospital_name,
    h.tier,
    h.teaching,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN hospitals h ON a.hospital_id = h.hospital_id
GROUP BY h.hospital_id, h.name, h.tier, h.teaching
HAVING total_admissions >= 500
ORDER BY readmission_rate_pct DESC
LIMIT 10;

-- C. Readmission by hospital tier
SELECT
    h.tier,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days,
    ROUND(AVG(h.beds), 0)                         AS avg_beds
FROM admissions a
JOIN hospitals h ON a.hospital_id = h.hospital_id
GROUP BY h.tier
ORDER BY h.tier;

-- D. Readmission by teaching status
SELECT
    h.teaching,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days
FROM admissions a
JOIN hospitals h ON a.hospital_id = h.hospital_id
GROUP BY h.teaching
ORDER BY h.teaching;
