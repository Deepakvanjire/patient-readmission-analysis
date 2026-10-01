# Power BI Dashboard Guide
## Patient Readmission Analysis — Synthetic Indian Hospital Data

> See `powerbi/dashboard_guide.md` for the full interactive dashboard setup guide.
> This file provides a reference summary for the docs folder.

---

## Dashboard Structure

| Page | Title | Focus |
|---|---|---|
| 1 | Executive Overview | KPIs and top-level readmission trends |
| 2 | Readmission Driver Analysis | Patient complexity factors |
| 3 | Hospital Performance | Hospital and state benchmarking |
| 4 | Historical Follow-Up Priority | Data-derived segmentation |

---

## Data Model

Star schema with:
- **DIM_PATIENTS** (patients table)
- **DIM_HOSPITALS** (hospitals table)
- **FACT_ADMISSIONS** (admissions table — central fact)
- **FACT_BILLING** (billing table)
- **FACT_DIAGNOSES** (diagnoses table)

---

## Key DAX Measures

| Measure | Formula Summary |
|---|---|
| Total Admissions | `COUNTROWS(admissions)` |
| Total Readmissions | `CALCULATE(COUNTROWS(...), readmitted_30d = 1)` |
| Readmission Rate | `DIVIDE([Total Readmissions], [Total Admissions], 0)` |
| Average LOS | `AVERAGE(admissions[los_days])` |
| Total Cost INR | `SUM(billing[total_cost_inr])` |
| Average Cost | `DIVIDE([Total Cost INR], [Total Admissions], 0)` |

Full DAX measures: see `powerbi/DAX_Measures.txt`

---

## Important Dashboard Labels

Page 4 must include this disclaimer text box:

> *"Historical Follow-Up Priority is based on historical patterns in a synthetic dataset.
> It does not constitute clinical advice or a validated readmission prediction model."*

---

## Connection Setup

1. Power BI Desktop → Get Data → MySQL Database
2. Server: `localhost` | Database: `patient_readmission`
3. Load all 5 tables
4. Set relationships per the star schema above
5. Add calculated columns (Priority Score, Followup Priority, Age Group)
