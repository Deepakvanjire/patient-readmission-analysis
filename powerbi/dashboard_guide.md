# Power BI Dashboard Guide
## Patient Readmission Analysis — Synthetic Indian Hospital Data

---

> **DISCLAIMER:** This project uses synthetic hospital data for analytical and portfolio purposes. All findings, segmentations, and follow-up priority assignments reflect historical patterns in the synthetic dataset only. They should not be interpreted as clinical diagnosis, medical advice, or validated clinical prediction models.

---

## 1. MySQL Connection Setup

1. Open **Power BI Desktop**
2. Click **Get Data → MySQL Database** (install MySQL connector if prompted)
3. Enter:
   - **Server:** `localhost`
   - **Database:** `patient_readmission`
4. Enter credentials: `root` / your password
5. Select all 5 tables: `patients`, `admissions`, `diagnoses`, `hospitals`, `billing`
6. Click **Load**

---

## 2. Data Model (Star Schema)

```
DIM_PATIENTS          DIM_HOSPITALS
patients[patient_id] ─┐   hospitals[hospital_id] ─┐
                       │                            │
                   FACT_ADMISSIONS (admissions)
                   admission_id (PK)
                   patient_id FK ──────────────────┘ (Many:1)
                   hospital_id FK ─────────────────── (Many:1)
                       │
              ┌─────────┴─────────┐
         FACT_BILLING         FACT_DIAGNOSES
         billing               diagnoses
         admission_id FK       admission_id FK
         (1:1 with admissions) (Many:1 with admissions)
```

### Relationship Settings
| From | To | Cardinality | Filter Direction |
|---|---|---|---|
| admissions[patient_id] | patients[patient_id] | Many:1 | Single |
| admissions[hospital_id] | hospitals[hospital_id] | Many:1 | Single |
| billing[admission_id] | admissions[admission_id] | 1:1 | Single |
| diagnoses[admission_id] | admissions[admission_id] | Many:1 | Both |

---

## 3. Calculated Columns to Add

In the **admissions** table, add these calculated columns:

**Age Group** (from patients table via RELATED):
```dax
Age Group =
VAR age = RELATED(patients[age])
RETURN
SWITCH(
    TRUE(),
    age <= 29, "18-29",
    age <= 44, "30-44",
    age <= 59, "45-59",
    age <= 74, "60-74",
    "75+"
)
```

**Priority Score:**
```dax
Priority Score =
VAR prev  = RELATED(patients[prev_admissions])
VAR comor = RELATED(patients[comorbidity_count])
VAR age   = RELATED(patients[age])
RETURN
    IF(prev >= 3, 3, 0)
  + IF(comor >= 3, 3, 0)
  + IF([charlson_index] >= 3, 3, 0)
  + IF(age >= 60, 2, 0)
  + IF([los_days] >= 7, 2, 0)
  + IF([admit_type] = "Emergency", 2, 0)
  + IF([discharge_type] = "LAMA", 3, 0)
  + IF([discharge_type] = "Referred", 2, 0)
  + IF([ward_type] = "ICU", 2, 0)
```

**Historical Follow-Up Priority:**
```dax
Followup Priority =
SWITCH(
    TRUE(),
    [Priority Score] >= 10, "HIGH",
    [Priority Score] >= 5,  "MEDIUM",
    "LOW"
)
```

---

## 4. Dashboard Pages

### PAGE 1 — Executive Overview

| Visual | Type | Fields |
|---|---|---|
| Total Patients | KPI Card | `Total Patients` |
| Total Admissions | KPI Card | `Total Admissions` |
| Readmission Rate | KPI Card | `Readmission Rate %` |
| Avg LOS | KPI Card | `Average LOS` |
| Total Cost | KPI Card | `Total Cost INR` |
| Readmission trend by year | Line Chart | admit_date[Year], `Readmission Rate` |
| Readmission by age group | Bar Chart | Age Group, `Readmission Rate` |
| Readmission by diagnosis | Bar Chart | diag_category, `Readmission Rate` |
| Readmission by insurance | Bar Chart | insurance_type, `Readmission Rate` |
| Readmission by hospital | Bar Chart | name, `Readmission Rate` |

---

### PAGE 2 — Readmission Driver Analysis

| Visual | Type | Fields |
|---|---|---|
| Readmission by prev admissions | Column Chart | prev_admissions, `Readmission Rate` |
| Readmission by comorbidity | Column Chart | comorbidity_count, `Readmission Rate` |
| Readmission by Charlson index | Column Chart | charlson_index (bucketed), `Readmission Rate` |
| Readmission by ward type | Bar Chart | ward_type, `Readmission Rate` |
| Readmission by admission type | Bar Chart | admit_type, `Readmission Rate` |
| Readmission by discharge type | Bar Chart | discharge_type, `Readmission Rate` |
| LOS vs Readmission | Scatter | los_days, readmitted_30d |

---

### PAGE 3 — Hospital Performance

| Visual | Type | Fields |
|---|---|---|
| Hospital readmission rate | Bar Chart | name, `Hospital Readmission Rate` |
| Hospital admissions | Bar Chart | name, `Hospital Total Admissions` |
| Hospital avg LOS | Bar Chart | name, `Hospital Avg LOS` |
| Hospital avg cost | Bar Chart | name, `Average Cost Per Admission` |
| Readmission by state | Map / Bar | state, `Readmission Rate` |
| Readmission by tier | Bar Chart | tier, `Readmission Rate` |
| Teaching vs Non-teaching | Bar Chart | teaching, `Readmission Rate` |

---

### PAGE 4 — Follow-Up Priority

> ⚠️ Label this page clearly: **"Historical Follow-Up Priority — Based on Synthetic Data"**
>
> Add a text box: *"This segmentation is based on historical patterns in a synthetic dataset. It does not constitute clinical advice or a validated readmission prediction model."*

| Visual | Type | Fields |
|---|---|---|
| Priority tier distribution | Donut / Bar | Followup Priority, count |
| Readmission rate by tier | Bar Chart | Followup Priority, `Readmission Rate` |
| Admissions table | Table | patient_id, age, comorbidity_count, prev_admissions, charlson_index, Followup Priority, readmitted_30d |
| Priority by age group | Matrix | Age Group, Followup Priority, `Readmission Rate` |
| Priority by diagnosis | Matrix | diag_category, Followup Priority, count |

---

## 5. Formatting Recommendations

- **Theme:** Light/professional (white background, dark text)
- **Colors:**
  - Readmitted: Red `#D64242`
  - Not Readmitted: Blue `#4A90D9`
  - HIGH priority: Red `#D64242`
  - MEDIUM priority: Amber `#F5A623`
  - LOW priority: Green `#417505`
- **Font:** Segoe UI (Power BI default)
- **Page size:** 1280 × 720 (16:9 widescreen)

---

## 6. Slicers to Add (All Pages)

- Year (from admit_date)
- State (from patients)
- Insurance Type (from patients)
- Hospital Tier (from hospitals)
- Ward Type (from admissions)

---

## 7. Publishing

1. Save as `PatientReadmission.pbix`
2. Place in `powerbi/` folder
3. For portfolio: publish to Power BI Service (free account)
4. Export page screenshots as PDF for README embed
