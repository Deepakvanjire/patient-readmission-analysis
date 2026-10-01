-- ============================================================
-- 09_readmission_by_ward.sql
-- Readmission Rate by Ward Type
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission by ward type
SELECT
    ward_type,
    COUNT(admission_id)                           AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct,
    ROUND(AVG(los_days), 2)                       AS avg_los_days,
    ROUND(AVG(num_procedures), 2)                 AS avg_procedures,
    ROUND(AVG(charlson_index), 2)                 AS avg_charlson
FROM admissions
GROUP BY ward_type
ORDER BY readmission_rate_pct DESC;

-- B. Ward type x discharge type interaction
SELECT
    ward_type,
    discharge_type,
    COUNT(admission_id)                           AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct
FROM admissions
GROUP BY ward_type, discharge_type
ORDER BY ward_type, readmission_rate_pct DESC;

-- C. Average LOS by ward (readmitted vs not)
SELECT
    ward_type,
    readmitted_30d,
    COUNT(admission_id)                           AS admissions,
    ROUND(AVG(los_days), 2)                       AS avg_los_days
FROM admissions
GROUP BY ward_type, readmitted_30d
ORDER BY ward_type, readmitted_30d;
