-- ============================================================
-- 12_followup_prioritization.sql
-- Historical Follow-Up Priority Segmentation
-- Patient Readmission Analysis Project
--
-- DISCLAIMER: This is an analytical segmentation based on
-- historical patterns in synthetic data. It is NOT a clinical
-- diagnosis or prediction model. Segmentation reflects
-- historical data-derived prioritization only.
-- ============================================================

USE patient_readmission;

-- A. Follow-up priority scoring
--    Scores are assigned based on historically observable
--    factors from the dataset. Each factor contributes
--    transparently documented points.
--
--    Scoring logic (all derived from dataset patterns):
--      prev_admissions >= 3           : +3
--      comorbidity_count >= 3         : +3
--      charlson_index >= 3            : +3
--      age >= 60                      : +2
--      los_days >= 7                  : +2
--      admit_type = 'Emergency'       : +2
--      discharge_type = 'LAMA'        : +3
--      discharge_type = 'Referred'    : +2
--      ward_type = 'ICU'              : +2
--
--    Priority tiers (total score):
--      0-4  : LOW    (historically lower readmission pattern)
--      5-9  : MEDIUM (historically moderate readmission pattern)
--      10+  : HIGH   (historically higher readmission pattern)

WITH scored AS (
    SELECT
        a.admission_id,
        a.patient_id,
        p.age,
        p.comorbidity_count,
        p.prev_admissions,
        p.insurance_type,
        p.state,
        a.charlson_index,
        a.los_days,
        a.admit_type,
        a.ward_type,
        a.discharge_type,
        a.readmitted_30d,
        h.name                                    AS hospital_name,
        h.tier,

        -- Transparent scoring
        (
            CASE WHEN p.prev_admissions >= 3       THEN 3 ELSE 0 END
          + CASE WHEN p.comorbidity_count >= 3     THEN 3 ELSE 0 END
          + CASE WHEN a.charlson_index >= 3        THEN 3 ELSE 0 END
          + CASE WHEN p.age >= 60                  THEN 2 ELSE 0 END
          + CASE WHEN a.los_days >= 7              THEN 2 ELSE 0 END
          + CASE WHEN a.admit_type = 'Emergency'   THEN 2 ELSE 0 END
          + CASE WHEN a.discharge_type = 'LAMA'    THEN 3 ELSE 0 END
          + CASE WHEN a.discharge_type = 'Referred'THEN 2 ELSE 0 END
          + CASE WHEN a.ward_type = 'ICU'          THEN 2 ELSE 0 END
        )                                          AS priority_score
    FROM admissions a
    JOIN patients p  ON a.patient_id  = p.patient_id
    JOIN hospitals h ON a.hospital_id = h.hospital_id
)
SELECT
    admission_id,
    patient_id,
    age,
    comorbidity_count,
    prev_admissions,
    insurance_type,
    state,
    charlson_index,
    los_days,
    admit_type,
    ward_type,
    discharge_type,
    hospital_name,
    tier,
    priority_score,
    CASE
        WHEN priority_score >= 10 THEN 'HIGH'
        WHEN priority_score >= 5  THEN 'MEDIUM'
        ELSE                           'LOW'
    END                                           AS followup_priority,
    readmitted_30d
FROM scored
ORDER BY priority_score DESC
LIMIT 1000;

-- B. Summary: readmission rate by follow-up priority tier
WITH scored AS (
    SELECT
        a.admission_id,
        a.readmitted_30d,
        (
            CASE WHEN p.prev_admissions >= 3       THEN 3 ELSE 0 END
          + CASE WHEN p.comorbidity_count >= 3     THEN 3 ELSE 0 END
          + CASE WHEN a.charlson_index >= 3        THEN 3 ELSE 0 END
          + CASE WHEN p.age >= 60                  THEN 2 ELSE 0 END
          + CASE WHEN a.los_days >= 7              THEN 2 ELSE 0 END
          + CASE WHEN a.admit_type = 'Emergency'   THEN 2 ELSE 0 END
          + CASE WHEN a.discharge_type = 'LAMA'    THEN 3 ELSE 0 END
          + CASE WHEN a.discharge_type = 'Referred'THEN 2 ELSE 0 END
          + CASE WHEN a.ward_type = 'ICU'          THEN 2 ELSE 0 END
        )                                          AS priority_score
    FROM admissions a
    JOIN patients p ON a.patient_id = p.patient_id
)
SELECT
    CASE
        WHEN priority_score >= 10 THEN 'HIGH'
        WHEN priority_score >= 5  THEN 'MEDIUM'
        ELSE                           'LOW'
    END                                           AS followup_priority,
    COUNT(*)                                      AS total_admissions,
    SUM(readmitted_30d)                           AS readmissions,
    ROUND(AVG(readmitted_30d) * 100, 2)           AS readmission_rate_pct
FROM scored
GROUP BY followup_priority
ORDER BY FIELD(followup_priority, 'HIGH', 'MEDIUM', 'LOW');
