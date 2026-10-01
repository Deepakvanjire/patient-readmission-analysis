# Business Questions
## Patient Readmission Analysis — Synthetic Indian Hospital Data

> **DISCLAIMER:** All findings are derived from synthetic data for portfolio purposes only.
> They should not be used for clinical decision-making.

---

## Primary Business Question

> **"Which patient profiles have the highest historical 30-day readmission rates, and which profiles should the hospital consider for intensive post-discharge follow-up based on historical data?"**

---

## Detailed Business Questions

### 1. What is the overall 30-day readmission rate?
- **SQL:** `01_overall_readmission.sql`
- **Expected:** ~11.84%
- **Relevance:** Establishes the baseline for all comparisons.

---

### 2. Which diagnosis categories show higher historical readmission rates?
- **SQL:** `02_readmission_by_diagnosis.sql`
- **Analysis:** Readmission rate per `diag_category` (primary diagnosis, rank = 1)
- **Expected output:** Some categories (e.g., Cardiovascular, Renal) expected to show higher rates.

---

### 3. Which age groups show higher historical readmission rates?
- **SQL:** `03_readmission_by_age.sql`
- **Age groups:** 18-29, 30-44, 45-59, 60-74, 75+
- **Expected:** Older patients (60+) typically show higher rates.

---

### 4. How does insurance type relate to readmission?
- **SQL:** `04_readmission_by_insurance.sql`
- **Categories:** Ayushman, ESI, Private, Unknown
- **Note:** Differences may reflect underlying patient complexity rather than insurance itself.

---

### 5. How does previous admission history relate to readmission?
- **SQL:** `05_readmission_by_previous_admissions.sql`
- **Expectation:** Patients with more prior admissions expected to show higher rates.

---

### 6. How does comorbidity count and Charlson index relate to readmission?
- **SQL:** `06_readmission_by_comorbidity.sql`
- **Expectation:** Higher comorbidity burden → higher historical readmission rate.

---

### 7. What is the readmission rate by ward type?
- **SQL:** `09_readmission_by_ward.sql`
- **Categories:** General, ICU, Private, Semi-Private
- **Expectation:** ICU patients may show different patterns due to severity.

---

### 8. What is the readmission rate by admission type?
- **SQL:** `10_readmission_by_admission_type.sql`
- **Categories:** Emergency, Elective, OPD, Trauma
- **Expectation:** Emergency admissions expected to show higher rates.

---

### 9. Which hospitals have higher/lower historical readmission rates?
- **SQL:** `07_readmission_by_hospital.sql`
- **Analysis:** Hospital-level rates adjusted for admission volume.
- **Note:** Differences may reflect patient mix, not hospital quality alone.

---

### 10. Which states show different readmission patterns?
- **SQL:** `08_readmission_by_state.sql`
- **Analysis:** Patient home state and hospital location state.

---

### 11. What is the financial impact associated with readmissions?
- **SQL:** `11_readmission_financial_impact.sql`
- **Analysis:** Compare average total cost, government subsidy, and out-of-pocket cost for readmitted vs. non-readmitted patients.

---

### 12. How does discharge type relate to readmission?
- **SQL:** `10_readmission_by_admission_type.sql`
- **Categories:** Recovered, LAMA, Referred, Expired
- **Expectation:** LAMA (Left Against Medical Advice) may show higher readmission rates.

---

### 13. Which patient/profile segments could be considered higher priority for post-discharge follow-up?
- **SQL:** `12_followup_prioritization.sql`
- **Python:** `analyze_data.py` (section 10)
- **Output:** Historical Follow-Up Priority (LOW / MEDIUM / HIGH)
- **Note:** Based on historical patterns; not a clinical prediction.

---

## Expected Key Findings

| Business Question | Expected Direction |
|---|---|
| Age 60+ vs 18-29 | Higher readmission in older groups |
| High Charlson vs Low | Higher readmission with higher index |
| 6+ prev admissions vs 0 | Higher readmission with more history |
| Emergency vs Elective | Higher in Emergency admissions |
| LAMA discharge vs Recovered | Higher in LAMA |
| ICU ward vs General | Higher or similar, driven by complexity |
| Readmission cost vs non-readmission | Higher cost for readmitted patients |
