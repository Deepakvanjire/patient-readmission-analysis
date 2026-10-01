-- ============================================================
-- 10_readmission_by_admission_type.sql
-- Readmission Rate by Admission Type and Discharge Type
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission by admit_type
SELECT
    admit_type,
    COUNT(admission_id)                           AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct,
    ROUND(AVG(los_days), 2)                       AS avg_los_days,
    ROUND(AVG(charlson_index), 2)                 AS avg_charlson
FROM admissions
GROUP BY admit_type
ORDER BY readmission_rate_pct DESC;

-- B. Readmission by discharge_type
SELECT
    discharge_type,
    COUNT(admission_id)                           AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct,
    ROUND(AVG(los_days), 2)                       AS avg_los_days
FROM admissions
GROUP BY discharge_type
ORDER BY readmission_rate_pct DESC;

-- C. Admission type x discharge type matrix
SELECT
    admit_type,
    discharge_type,
    COUNT(admission_id)                           AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct
FROM admissions
GROUP BY admit_type, discharge_type
ORDER BY admit_type, readmission_rate_pct DESC;

-- D. Length of stay distribution by admission type (readmitted vs not)
SELECT
    admit_type,
    readmitted_30d,
    COUNT(admission_id)                           AS admissions,
    ROUND(AVG(los_days), 2)                       AS avg_los,
    MIN(los_days)                                 AS min_los,
    MAX(los_days)                                 AS max_los
FROM admissions
GROUP BY admit_type, readmitted_30d
ORDER BY admit_type, readmitted_30d;
