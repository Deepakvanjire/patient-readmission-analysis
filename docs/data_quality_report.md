# Data Quality Report
## Patient Readmission Analysis — Synthetic Indian Hospital Data

> **DISCLAIMER:** All data is synthetic and generated for portfolio/analytical purposes only.

---

## 1. Row Counts

| Table | Expected | Actual | Status |
|---|---|---|---|
| patients | 86,400 | 86,400 | ✅ Pass |
| admissions | 120,000 | 120,000 | ✅ Pass |
| diagnoses | 271,341 | 271,341 | ✅ Pass |
| hospitals | 33 | 33 | ✅ Pass |
| billing | 120,000 | 120,000 | ✅ Pass |

---

## 2. Column Counts

| Table | Columns |
|---|---|
| patients | 8 |
| admissions | 17 |
| diagnoses | 6 |
| hospitals | 6 |
| billing | 6 |

---

## 3. Duplicate Checks

### Exact Row Duplicates (removed during cleaning)

| Table | Duplicates Found | Duplicates Removed |
|---|---|---|
| patients | 0 | 0 |
| admissions | 0 | 0 |
| diagnoses | 0 | 0 |
| hospitals | 0 | 0 |
| billing | 0 | 0 |

### Primary Key Duplicate Check

| Table | Primary Key | Duplicates |
|---|---|---|
| patients | patient_id | 0 ✅ |
| admissions | admission_id | 0 ✅ |
| diagnoses | diag_id | 0 ✅ |
| hospitals | hospital_id | 0 ✅ |
| billing | bill_id | 0 ✅ |

---

## 4. Missing Value Report

### Before Cleaning
| Table | Column | Missing Count | Action Taken |
|---|---|---|---|
| patients | insurance_type | 24,715 | Replaced with `Unknown` |

### After Cleaning
| Table | Missing Values |
|---|---|
| patients | 0 ✅ |
| admissions | 0 ✅ |
| diagnoses | 0 ✅ |
| hospitals | 0 ✅ |
| billing | 0 ✅ |

---

## 5. Primary Key Integrity

All primary keys are valid UUIDs stored as strings.

No duplicate primary keys detected across any table.

Primary keys are preserved as strings and are not converted to integers.

---

## 6. Foreign Key Integrity

| Relationship | Broken References |
|---|---|
| admissions → patients | 0 ✅ |
| admissions → hospitals | 0 ✅ |
| diagnoses → admissions | 0 ✅ |
| billing → admissions | 0 ✅ |

---

## 7. Data Type Checks

| Table | Column | Expected Type | Status |
|---|---|---|---|
| patients | patient_id | String/UUID | ✅ |
| patients | age | Integer | ✅ |
| patients | comorbidity_count | Integer | ✅ |
| patients | prev_admissions | Integer | ✅ |
| admissions | admission_id | String/UUID | ✅ |
| admissions | admit_date | Date | ✅ |
| admissions | discharge_date | Date | ✅ |
| admissions | los_days | Integer | ✅ |
| admissions | readmitted_30d | Integer (0/1) | ✅ |
| admissions | hba1c | Float | ✅ |
| billing | total_cost_inr | Float | ✅ |
| billing | out_of_pocket_inr | Float | ✅ |

---

## 8. Date Validation

| Check | Result |
|---|---|
| admit_date ≤ discharge_date | All valid ✅ |
| Dates within plausible range (2000–2030) | All valid ✅ |
| No null dates | All valid ✅ |

---

## 9. Numeric Range Checks

| Column | Min | Max | Expected Range | Status |
|---|---|---|---|---|
| age | 18 | ~100 | 0–130 | ✅ |
| los_days | 1 | ~30+ | 0–365 | ✅ |
| charlson_index | 0 | ~10+ | 0–50 | ✅ |
| comorbidity_count | 0 | 6 | 0–20 | ✅ |
| prev_admissions | 0 | 10 | 0–50 | ✅ |
| total_cost_inr | >0 | <10M | >0 | ✅ |
| out_of_pocket_inr | ≥0 | — | ≥0 | ✅ |

---

## 10. Readmission Distribution

| readmitted_30d | Count | Percentage |
|---|---|---|
| 0 (Not Readmitted) | 105,790 | 88.16% |
| 1 (Readmitted) | 14,210 | 11.84% |

**Overall 30-day readmission rate: 11.84%**

This rate is typical of datasets used in hospital readmission analysis literature (common range: 10–20%).

---

## 11. Insurance Type Distribution

| Insurance Type | Patient Count |
|---|---|
| Ayushman | 25,967 |
| Unknown | 24,715 |
| Private | 21,372 |
| ESI | 14,346 |

> `Unknown` records represent patients whose insurance information was not captured. These are retained as a valid category in the analysis.

---

## 12. Data Quality Summary

| Category | Issues Found | Status |
|---|---|---|
| Row counts | None | ✅ Pass |
| Duplicates | None | ✅ Pass |
| Missing values | Resolved (insurance) | ✅ Pass |
| Primary keys | None | ✅ Pass |
| Foreign keys | None | ✅ Pass |
| Date validity | None | ✅ Pass |
| Numeric ranges | None | ✅ Pass |
| Readmission rate | ~11.84% | ✅ Plausible |

**The dataset is clean and ready for analysis.**
