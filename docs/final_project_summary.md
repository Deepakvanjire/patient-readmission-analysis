# Final Project Summary
## Patient Readmission Analysis & Hospital Follow-Up Intelligence System

---

> **⚠️ IMPORTANT LIMITATION STATEMENT:**
> "This project uses synthetic hospital data for analytical and portfolio purposes. The historical patterns and follow-up prioritization presented here should not be interpreted as clinical diagnosis, medical advice, or a validated clinical prediction model."

---

## Project Title
Patient Readmission Analysis & Hospital Follow-Up Intelligence System

---

## Business Problem

Hospital 30-day readmissions are a key indicator of healthcare quality, patient outcomes, and operational costs. This project identifies which historical patient and admission profiles are associated with higher readmission rates in the synthetic dataset, and constructs a transparent follow-up priority segmentation.

**Primary question:**
> "Which patient profiles have the highest historical 30-day readmission rates, and which profiles should the hospital consider for intensive post-discharge follow-up?"

---

## Dataset

| Table | Rows | Description |
|---|---|---|
| patients | 86,400 | Demographics, insurance, comorbidities |
| admissions | 120,000 | Clinical data, diagnoses, readmission flags |
| diagnoses | 271,341 | ICD-10 coded diagnoses per admission |
| hospitals | 33 | Hospital metadata |
| billing | 120,000 | Cost and subsidy records |

**All data is synthetic. No real patient data was used.**

---

## Data Quality

| Check | Result |
|---|---|
| Duplicate records | 0 across all tables |
| Missing values after cleaning | 0 |
| FK integrity issues | 0 |
| Date validity issues | 0 |
| Primary key conflicts | 0 |

---

## Key Metrics

| Metric | Value |
|---|---|
| Total Patients | 86,400 |
| Total Admissions | 120,000 |
| 30-Day Readmissions | 14,210 |
| **30-Day Readmission Rate** | **11.84%** |
| 7-Day Readmission Rate | (see database) |
| Total Diagnoses | 271,341 |
| Number of Hospitals | 33 |

---

## Key Findings (Synthetic Dataset)

### Age & Demographics
- Older age groups (60-74, 75+) show historically higher readmission rates
- Gender differences are minimal in this synthetic dataset

### Clinical Complexity
- Comorbidity count ≥ 3: associated with higher readmission
- Charlson index ≥ 3: associated with elevated readmission in the dataset
- Higher number of previous admissions: strongest individual predictor in the scoring model

### Admission & Discharge Characteristics
- **Emergency admissions** show higher rates than Elective/OPD
- **LAMA (Left Against Medical Advice) discharge** shows the highest readmission rate of all discharge types
- **ICU ward** admissions show higher rates, consistent with greater clinical complexity
- Longer length of stay (≥ 7 days) associated with higher readmission rates

### Insurance & Economics
- Insurance type differences observed; likely reflect patient complexity differences
- Readmitted patients have higher average total cost, government subsidy, and out-of-pocket burden

### Hospital & Geography
- Hospital-level variation exists; unadjusted for case mix
- State-level patterns observed; reflect synthetic data distribution

---

## SQL Insights

12 SQL analytical files were developed covering:
- Overall readmission rate (baseline ~11.84%)
- Readmission by diagnosis category, age group, insurance, previous admissions
- Comorbidity and Charlson index analysis
- Hospital, state, ward, admission type, and discharge type analysis
- Financial impact quantification
- Transparent follow-up priority scoring

---

## Python Insights

10 professional charts generated including:
- Readmission donut + year trend
- Readmission by age group (colour-coded above/below average)
- Readmission by diagnosis category
- Readmission by insurance type
- Readmission by previous admissions (line chart with trend)
- Readmission by comorbidity count
- Readmission by hospital (horizontal bar)
- Readmission by state (horizontal bar)
- Financial comparison (total cost, subsidy, OOP)
- Historical follow-up priority distribution and rates

---

## Power BI Dashboard

4-page interactive dashboard:

| Page | Content |
|---|---|
| Executive Overview | KPIs, year trend, top-level breakdowns |
| Readmission Driver Analysis | Clinical complexity factors |
| Hospital Performance | Hospital and state benchmarks |
| Historical Follow-Up Priority | Segmentation analysis |

---

## Historical Follow-Up Priority

A transparent, rule-based segmentation was developed based on 9 observable dataset factors:

| Tier | Score | Approx % | Description |
|---|---|---|---|
| HIGH | ≥ 10 | ~24% | Historically higher readmission pattern |
| MEDIUM | 5–9 | ~41% | Historically moderate readmission pattern |
| LOW | 0–4 | ~35% | Historically lower readmission pattern |

**This is NOT a clinical prediction tool. It reflects historical patterns only.**

---

## Financial Insights

- Readmitted admissions have higher average total cost than non-readmitted
- Government subsidy is higher for readmitted patients
- Out-of-pocket burden is also elevated for readmitted patients
- LAMA discharges and Emergency admissions account for disproportionate cost

---

## Limitations

1. All data is **synthetic** — no real patients or hospitals
2. Follow-up priority is **descriptive**, not a clinical prediction model
3. Hospital comparisons are **unadjusted** for patient case mix
4. Associations are **correlational**, not causal
5. No external validation of any analytical finding
6. In real healthcare settings, readmission definitions, data availability, and patient populations vary substantially

---

## Future Improvements

1. Apply logistic regression or random forest for readmission prediction (synthetic experiment)
2. Add risk-standardized hospital readmission rates (case-mix adjustment)
3. Include discharge medication data and follow-up appointment data
4. Temporal analysis — rolling 30-day readmission windows
5. Survival/time-to-readmission analysis using synthetic dates
6. Expand to 90-day readmission analysis

---

## Technologies Used

Python · Pandas · NumPy · Matplotlib · MySQL 8.0 · SQL · Power BI · DAX · mysql-connector-python · python-dotenv · Scikit-learn (optional)

---

*Generated: 2026 | Portfolio Project | Synthetic Data Only*
