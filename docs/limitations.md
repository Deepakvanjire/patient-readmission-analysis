# Limitations
## Patient Readmission Analysis — Synthetic Indian Hospital Data

> **DISCLAIMER:** This project uses synthetic hospital data for analytical and portfolio purposes only.

---

## 1. Synthetic Data

- **All data is synthetic.** No real patient records were used.
- The dataset was designed to produce realistic analytical patterns, but individual values, relationships, and trends do not reflect real hospital performance.
- Comparisons between hospitals, states, or patient groups should not be interpreted as real-world findings.

---

## 2. Readmission Target Variable

- `readmitted_30d` is a pre-embedded synthetic flag. It was not derived from observing actual 30-day post-discharge outcomes.
- The overall readmission rate (~11.84%) was built into the dataset design, not measured from real admissions.
- In real-world datasets, readmission definitions vary by hospital policy and data system.

---

## 3. Follow-Up Priority Segmentation

- The **Historical Follow-Up Priority** (LOW / MEDIUM / HIGH) is a **descriptive analytical segmentation**, not a clinical decision support tool.
- Scoring weights are chosen for transparency and interpretability, not derived from statistical regression or machine learning optimization.
- The segmentation has **not been validated** on real patient data.
- It does not account for variable interactions, patient preferences, or clinical context.
- **Do not use this segmentation for clinical decision-making.**

---

## 4. Causal Inference

- All associations in this analysis are **descriptive correlations**, not causal relationships.
- For example: higher Charlson index being associated with higher readmission rates does not imply that the index *causes* readmission.
- No causal inference methods (propensity scoring, instrumental variables, etc.) were applied.

---

## 5. Optional Machine Learning Model

- If a logistic regression or random forest model is trained, it is trained on **synthetic data only**.
- Model performance metrics (accuracy, recall, ROC-AUC) apply to this synthetic dataset only and cannot be generalized.
- The model is **not validated** on any external dataset.
- It should not be described as a clinical prediction tool.

---

## 6. Missing Data

- The only missing data in the original dataset was `insurance_type` (24,715 records).
- These were labeled as `Unknown` — a transparent, documented category rather than imputed values.
- Other columns have no missing data, which may itself be a characteristic of the synthetic generation process (real-world data commonly has more missing values).

---

## 7. Hospital and State Comparisons

- Hospital-level readmission rate comparisons are unadjusted for patient case mix.
- Hospitals treating more complex or emergency patients may appear to have higher rates, not because of lower quality care, but due to patient composition.
- Case-mix adjustment (e.g., risk-standardized readmission rates) was not applied.

---

## 8. Time Period and Temporal Validity

- The dataset covers synthetic admissions over multiple years.
- No temporal cross-validation was performed.
- Clinical practices, policies, and healthcare systems change over time; historical patterns may not predict future patterns.

---

## 9. Indian Healthcare Context

- Insurance type categories (Ayushman Bharat, ESI) are included to reflect an Indian healthcare context.
- The synthetic data does not accurately capture the true complexity of healthcare delivery, insurance coverage, or patient demographics across India.

---

## 10. Portfolio Use Only

This project is designed to demonstrate data engineering, SQL, Python, and Power BI skills in a portfolio setting.

It should not be:
- Used in real clinical environments
- Presented as evidence-based clinical research
- Used to make decisions about real patients or hospitals

---

## Summary of Risk Areas

| Area | Risk Level | Mitigation |
|---|---|---|
| Treating synthetic patterns as real | HIGH | Clear disclaimers throughout |
| Using follow-up priority as diagnosis | HIGH | Labelled as descriptive segmentation only |
| Generalizing ML model | HIGH | Clearly labelled as synthetic experiment |
| Hospital benchmarking without case-mix | MEDIUM | Noted in methodology |
| Missing data imputation effects | LOW | Only one column imputed, documented |
