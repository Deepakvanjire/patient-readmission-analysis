-- ============================================================
-- 01_overall_readmission.sql
-- Overall 30-Day Readmission Rate
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Total admissions and readmissions
SELECT
    COUNT(*)                                      AS total_admissions,
    SUM(readmitted_30d)                           AS total_readmissions,
    COUNT(*) - SUM(readmitted_30d)                AS not_readmitted,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct,
    ROUND(AVG(los_days), 2)                       AS avg_los_days,
    ROUND(AVG(num_procedures), 2)                 AS avg_procedures
FROM admissions;

-- B. Readmission by year
SELECT
    YEAR(admit_date)                              AS admit_year,
    COUNT(*)                                      AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct
FROM admissions
GROUP BY YEAR(admit_date)
ORDER BY admit_year;

-- C. Readmission by month (seasonal pattern)
SELECT
    MONTH(admit_date)                             AS admit_month,
    MONTHNAME(admit_date)                         AS month_name,
    COUNT(*)                                      AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct
FROM admissions
GROUP BY MONTH(admit_date), MONTHNAME(admit_date)
ORDER BY admit_month;

-- D. 7-day vs 30-day readmission comparison
SELECT
    SUM(readmitted_7d)                            AS readmitted_7d,
    SUM(readmitted_30d)                           AS readmitted_30d,
    ROUND(AVG(readmitted_7d)  * 100, 2)           AS rate_7d_pct,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS rate_30d_pct
FROM admissions;
