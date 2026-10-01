-- ============================================================
-- 11_readmission_financial_impact.sql
-- Financial Impact of Readmissions
-- Patient Readmission Analysis Project
-- ============================================================

USE patient_readmission;

-- A. Overall financial summary (readmitted vs not)
SELECT
    a.readmitted_30d,
    COUNT(a.admission_id)                         AS total_admissions,
    ROUND(SUM(b.total_cost_inr), 0)               AS total_cost_inr,
    ROUND(AVG(b.total_cost_inr), 0)               AS avg_cost_per_admission,
    ROUND(SUM(b.govt_subsidy_inr), 0)             AS total_govt_subsidy,
    ROUND(AVG(b.govt_subsidy_inr), 0)             AS avg_govt_subsidy,
    ROUND(SUM(b.out_of_pocket_inr), 0)            AS total_out_of_pocket,
    ROUND(AVG(b.out_of_pocket_inr), 0)            AS avg_out_of_pocket
FROM admissions a
JOIN billing b ON a.admission_id = b.admission_id
GROUP BY a.readmitted_30d;

-- B. Financial impact by cost category
SELECT
    b.cost_category,
    COUNT(a.admission_id)                         AS total_admissions,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct,
    ROUND(AVG(b.total_cost_inr), 0)               AS avg_cost_inr
FROM admissions a
JOIN billing b ON a.admission_id = b.admission_id
GROUP BY b.cost_category
ORDER BY avg_cost_inr DESC;

-- C. Financial impact by insurance type (avg cost + subsidy)
SELECT
    p.insurance_type,
    COUNT(a.admission_id)                         AS total_admissions,
    ROUND(AVG(b.total_cost_inr), 0)               AS avg_total_cost,
    ROUND(AVG(b.govt_subsidy_inr), 0)             AS avg_govt_subsidy,
    ROUND(AVG(b.out_of_pocket_inr), 0)            AS avg_out_of_pocket,
    SUM(a.readmitted_30d)                         AS readmissions,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN billing b ON a.admission_id = b.admission_id
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.insurance_type
ORDER BY avg_out_of_pocket DESC;

-- D. Total readmission financial burden estimate
SELECT
    SUM(CASE WHEN a.readmitted_30d = 1 THEN b.total_cost_inr ELSE 0 END)      AS readmission_total_cost_inr,
    SUM(CASE WHEN a.readmitted_30d = 1 THEN b.out_of_pocket_inr ELSE 0 END)   AS readmission_oop_inr,
    SUM(CASE WHEN a.readmitted_30d = 1 THEN b.govt_subsidy_inr ELSE 0 END)    AS readmission_subsidy_inr,
    COUNT(CASE WHEN a.readmitted_30d = 1 THEN 1 END)                          AS total_readmissions
FROM admissions a
JOIN billing b ON a.admission_id = b.admission_id;

-- E. Financial impact by hospital
SELECT
    h.name                                        AS hospital_name,
    h.tier,
    COUNT(a.admission_id)                         AS total_admissions,
    ROUND(AVG(b.total_cost_inr), 0)               AS avg_cost_inr,
    ROUND(AVG(a.readmitted_30d) * 100, 2)         AS readmission_rate_pct
FROM admissions a
JOIN billing b ON a.admission_id = b.admission_id
JOIN hospitals h ON a.hospital_id = h.hospital_id
GROUP BY h.hospital_id, h.name, h.tier
ORDER BY avg_cost_inr DESC;
