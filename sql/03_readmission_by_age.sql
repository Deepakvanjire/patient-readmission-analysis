-- ============================================================
-- 03_readmission_by_age.sql
-- Readmission Rate by Age Group
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Readmission rate by age group
SELECT
    CASE
        WHEN p.age BETWEEN 18 AND 29 THEN '18-29'
        WHEN p.age BETWEEN 30 AND 44 THEN '30-44'
        WHEN p.age BETWEEN 45 AND 59 THEN '45-59'
        WHEN p.age BETWEEN 60 AND 74 THEN '60-74'
        WHEN p.age >= 75             THEN '75+'
        ELSE 'Under 18 / Unknown'
    END                                           AS age_group,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(a.los_days), 2)                     AS avg_los_days,
    ROUND(AVG(a.charlson_index), 2)               AS avg_charlson_index
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY age_group
ORDER BY
    FIELD(age_group, '18-29', '30-44', '45-59', '60-74', '75+', 'Under 18 / Unknown');

-- B. Readmission by age group and gender
SELECT
    CASE
        WHEN p.age BETWEEN 18 AND 29 THEN '18-29'
        WHEN p.age BETWEEN 30 AND 44 THEN '30-44'
        WHEN p.age BETWEEN 45 AND 59 THEN '45-59'
        WHEN p.age BETWEEN 60 AND 74 THEN '60-74'
        WHEN p.age >= 75             THEN '75+'
        ELSE 'Other'
    END                                           AS age_group,
    p.gender,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY age_group, p.gender
ORDER BY
    FIELD(age_group, '18-29', '30-44', '45-59', '60-74', '75+', 'Other'),
    p.gender;

-- C. Average age of readmitted vs non-readmitted
SELECT
    readmitted_30d,
    ROUND(AVG(p.age), 1)                          AS avg_age,
    ROUND(MIN(p.age), 0)                          AS min_age,
    ROUND(MAX(p.age), 0)                          AS max_age
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY readmitted_30d;
