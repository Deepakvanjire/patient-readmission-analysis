import pandas as pd
from pathlib import Path

# ============================================================
# PATIENT READMISSION ANALYSIS
# DATA CLEANING SCRIPT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw_data"
CLEAN_DIR = BASE_DIR / "cleaned_data"

CLEAN_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("PATIENT READMISSION ANALYSIS - DATA CLEANING")
print("=" * 60)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("\nLoading datasets...")

patients = pd.read_csv(RAW_DIR / "patients.csv")
admissions = pd.read_csv(RAW_DIR / "admissions.csv")
diagnoses = pd.read_csv(RAW_DIR / "diagnoses.csv")
hospitals = pd.read_csv(RAW_DIR / "hospitals.csv")
billing = pd.read_csv(RAW_DIR / "billing.csv")

print("All datasets loaded successfully.")


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

datasets = {
    "PATIENTS": patients,
    "ADMISSIONS": admissions,
    "DIAGNOSES": diagnoses,
    "HOSPITALS": hospitals,
    "BILLING": billing
}

for df in datasets.values():
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )


# ============================================================
# 3. ORIGINAL DATASET SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ORIGINAL DATASET SUMMARY")
print("=" * 60)

for name, df in datasets.items():
    print(f"\n{name}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicates: {df.duplicated().sum():,}")


# ============================================================
# 4. REMOVE EXACT DUPLICATES
# ============================================================

print("\n" + "=" * 60)
print("REMOVING DUPLICATES")
print("=" * 60)

for name, df in datasets.items():

    before = len(df)

    df.drop_duplicates(inplace=True)

    after = len(df)

    print(
        f"{name}: Removed {before - after:,} duplicate rows"
    )


# ============================================================
# 5. CLEAN PATIENT DATA
# ============================================================

print("\nCleaning patient data...")

# IMPORTANT:
# IDs are kept as strings so their original format is preserved.

patients["patient_id"] = (
    patients["patient_id"]
    .astype("string")
    .str.strip()
)

patients["gender"] = (
    patients["gender"]
    .astype("string")
    .str.strip()
)

patients["state"] = (
    patients["state"]
    .astype("string")
    .str.strip()
)

patients["bpl_card"] = (
    patients["bpl_card"]
    .astype("string")
    .str.strip()
)

patients["age"] = pd.to_numeric(
    patients["age"],
    errors="coerce"
)

patients["comorbidity_count"] = pd.to_numeric(
    patients["comorbidity_count"],
    errors="coerce"
)

patients["prev_admissions"] = pd.to_numeric(
    patients["prev_admissions"],
    errors="coerce"
)

# Missing insurance = Unknown
patients["insurance_type"] = (
    patients["insurance_type"]
    .fillna("Unknown")
    .astype("string")
    .str.strip()
)

patients["insurance_type"] = (
    patients["insurance_type"]
    .replace("", "Unknown")
)


# ============================================================
# 6. CLEAN ADMISSIONS DATA
# ============================================================

print("Cleaning admissions data...")

# Keep IDs as strings
admissions["admission_id"] = (
    admissions["admission_id"]
    .astype("string")
    .str.strip()
)

admissions["patient_id"] = (
    admissions["patient_id"]
    .astype("string")
    .str.strip()
)

admissions["hospital_id"] = (
    admissions["hospital_id"]
    .astype("string")
    .str.strip()
)

# Dates
admissions["admit_date"] = pd.to_datetime(
    admissions["admit_date"],
    errors="coerce"
)

admissions["discharge_date"] = pd.to_datetime(
    admissions["discharge_date"],
    errors="coerce"
)

# Numeric columns
numeric_columns = [
    "los_days",
    "num_procedures",
    "charlson_index",
    "hba1c",
    "creatinine",
    "haemoglobin",
    "systolic_bp",
    "readmitted_30d",
    "readmitted_7d"
]

for column in numeric_columns:
    admissions[column] = pd.to_numeric(
        admissions[column],
        errors="coerce"
    )

# Text columns
for column in [
    "admit_type",
    "ward_type",
    "discharge_type"
]:
    admissions[column] = (
        admissions[column]
        .astype("string")
        .str.strip()
    )


# ============================================================
# 7. CLEAN DIAGNOSES DATA
# ============================================================

print("Cleaning diagnosis data...")

# Keep IDs as strings
diagnoses["diag_id"] = (
    diagnoses["diag_id"]
    .astype("string")
    .str.strip()
)

diagnoses["admission_id"] = (
    diagnoses["admission_id"]
    .astype("string")
    .str.strip()
)

diagnoses["icd10_code"] = (
    diagnoses["icd10_code"]
    .astype("string")
    .str.strip()
)

diagnoses["diag_desc"] = (
    diagnoses["diag_desc"]
    .astype("string")
    .str.strip()
)

diagnoses["diag_category"] = (
    diagnoses["diag_category"]
    .astype("string")
    .str.strip()
)

diagnoses["diag_rank"] = pd.to_numeric(
    diagnoses["diag_rank"],
    errors="coerce"
)


# ============================================================
# 8. CLEAN HOSPITAL DATA
# ============================================================

print("Cleaning hospital data...")

hospitals["hospital_id"] = (
    hospitals["hospital_id"]
    .astype("string")
    .str.strip()
)

hospitals["name"] = (
    hospitals["name"]
    .astype("string")
    .str.strip()
)

hospitals["state"] = (
    hospitals["state"]
    .astype("string")
    .str.strip()
)

hospitals["tier"] = (
    hospitals["tier"]
    .astype("string")
    .str.strip()
)

hospitals["teaching"] = (
    hospitals["teaching"]
    .astype("string")
    .str.strip()
)

hospitals["beds"] = pd.to_numeric(
    hospitals["beds"],
    errors="coerce"
)


# ============================================================
# 9. CLEAN BILLING DATA
# ============================================================

print("Cleaning billing data...")

billing["bill_id"] = (
    billing["bill_id"]
    .astype("string")
    .str.strip()
)

billing["admission_id"] = (
    billing["admission_id"]
    .astype("string")
    .str.strip()
)

billing["total_cost_inr"] = pd.to_numeric(
    billing["total_cost_inr"],
    errors="coerce"
)

billing["govt_subsidy_inr"] = pd.to_numeric(
    billing["govt_subsidy_inr"],
    errors="coerce"
)

billing["out_of_pocket_inr"] = pd.to_numeric(
    billing["out_of_pocket_inr"],
    errors="coerce"
)

billing["cost_category"] = (
    billing["cost_category"]
    .astype("string")
    .str.strip()
)


# ============================================================
# 10. PRIMARY KEY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PRIMARY KEY VALIDATION")
print("=" * 60)

print(
    "Duplicate patient_id:",
    patients["patient_id"].duplicated().sum()
)

print(
    "Duplicate admission_id:",
    admissions["admission_id"].duplicated().sum()
)

print(
    "Duplicate hospital_id:",
    hospitals["hospital_id"].duplicated().sum()
)

print(
    "Duplicate bill_id:",
    billing["bill_id"].duplicated().sum()
)


# ============================================================
# 11. RELATIONSHIP VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("TABLE RELATIONSHIP VALIDATION")
print("=" * 60)

admissions_without_patient = (
    ~admissions["patient_id"].isin(
        patients["patient_id"]
    )
).sum()

admissions_without_hospital = (
    ~admissions["hospital_id"].isin(
        hospitals["hospital_id"]
    )
).sum()

diagnoses_without_admission = (
    ~diagnoses["admission_id"].isin(
        admissions["admission_id"]
    )
).sum()

billing_without_admission = (
    ~billing["admission_id"].isin(
        admissions["admission_id"]
    )
).sum()

print(
    "Admissions without patient:",
    admissions_without_patient
)

print(
    "Admissions without hospital:",
    admissions_without_hospital
)

print(
    "Diagnoses without admission:",
    diagnoses_without_admission
)

print(
    "Billing without admission:",
    billing_without_admission
)


# ============================================================
# 12. READMISSION CHECK
# ============================================================

print("\n" + "=" * 60)
print("30-DAY READMISSION CHECK")
print("=" * 60)

print(
    admissions["readmitted_30d"]
    .value_counts(dropna=False)
    .sort_index()
)

readmission_rate = (
    admissions["readmitted_30d"].mean() * 100
)

print(
    f"\n30-Day Readmission Rate: {readmission_rate:.2f}%"
)


# ============================================================
# 13. MISSING VALUE CHECK
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUE CHECK")
print("=" * 60)

for name, df in datasets.items():

    missing = df.isna().sum()

    missing = missing[missing > 0]

    print(f"\n{name}")

    if len(missing) == 0:
        print("No missing values.")
    else:
        print(missing)


# ============================================================
# 14. INSURANCE DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("INSURANCE TYPE DISTRIBUTION")
print("=" * 60)

print(
    patients["insurance_type"]
    .value_counts(dropna=False)
)


# ============================================================
# 15. SAVE CLEANED DATA
# ============================================================

print("\n" + "=" * 60)
print("SAVING CLEANED DATA")
print("=" * 60)

patients.to_csv(
    CLEAN_DIR / "patients_clean.csv",
    index=False
)

admissions.to_csv(
    CLEAN_DIR / "admissions_clean.csv",
    index=False
)

diagnoses.to_csv(
    CLEAN_DIR / "diagnoses_clean.csv",
    index=False
)

hospitals.to_csv(
    CLEAN_DIR / "hospitals_clean.csv",
    index=False
)

billing.to_csv(
    CLEAN_DIR / "billing_clean.csv",
    index=False
)

print("\nCleaned files saved successfully:")

print("✓ patients_clean.csv")
print("✓ admissions_clean.csv")
print("✓ diagnoses_clean.csv")
print("✓ hospitals_clean.csv")
print("✓ billing_clean.csv")


# ============================================================
# 16. COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)