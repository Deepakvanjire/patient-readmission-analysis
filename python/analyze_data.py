"""
============================================================
PATIENT READMISSION ANALYSIS
Data Analysis Script
============================================================
Generates descriptive analysis charts and the Historical
Follow-Up Priority segmentation from cleaned CSV files.

All outputs are saved to python/output/

DISCLAIMER: This project uses synthetic hospital data for
analytical and portfolio purposes. The historical patterns
and follow-up prioritization presented here should not be
interpreted as clinical diagnosis, medical advice, or a
validated clinical prediction model.

Usage:
    python analyze_data.py
============================================================
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "cleaned_data"
OUT_DIR   = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(exist_ok=True)

PALETTE = {
    "readmitted":     "#E05252",
    "not_readmitted": "#4A90D9",
    "neutral":        "#5B8DB8",
    "high":           "#D64242",
    "medium":         "#F5A623",
    "low":            "#417505",
    "bg":             "#F8F9FA",
    "grid":           "#DEE2E6",
}

plt.rcParams.update({
    "figure.facecolor": PALETTE["bg"],
    "axes.facecolor":   PALETTE["bg"],
    "axes.grid":        True,
    "grid.color":       PALETTE["grid"],
    "grid.linewidth":   0.6,
    "font.family":      "sans-serif",
    "font.size":        11,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})

print("=" * 60)
print("PATIENT READMISSION ANALYSIS - Data Analysis")
print("DISCLAIMER: Synthetic data, for portfolio purposes only.")
print("=" * 60)

# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading cleaned datasets...")

patients   = pd.read_csv(CLEAN_DIR / "patients_clean.csv",   dtype={"patient_id": str})
admissions = pd.read_csv(CLEAN_DIR / "admissions_clean.csv", dtype={"admission_id": str, "patient_id": str, "hospital_id": str},
                         parse_dates=["admit_date", "discharge_date"])
hospitals  = pd.read_csv(CLEAN_DIR / "hospitals_clean.csv",  dtype={"hospital_id": str})
billing    = pd.read_csv(CLEAN_DIR / "billing_clean.csv",    dtype={"bill_id": str, "admission_id": str})

# Merged base
base = admissions.merge(patients,  on="patient_id",  how="left")
base = base.merge(hospitals, on="hospital_id", how="left")
base = base.merge(billing,   on="admission_id", how="left")

print(f"Merged dataset: {len(base):,} rows")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def save_fig(filename, fig=None):
    path = OUT_DIR / filename
    if fig:
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
    print(f"  Saved: {filename}")


def readmission_rate(df):
    return df["readmitted_30d"].mean() * 100


def bar_chart(ax, x, y, color=None, **kwargs):
    bars = ax.bar(x, y, color=color or PALETTE["neutral"], edgecolor="white", linewidth=0.5, **kwargs)
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
    return bars


# ============================================================
# 1. OVERALL READMISSION RATE
# ============================================================

print("\n[1] Overall readmission rate...")

overall_rate = readmission_rate(admissions)
total_adm    = len(admissions)
total_read   = admissions["readmitted_30d"].sum()
avg_los      = admissions["los_days"].mean()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Overall 30-Day Readmission Rate  |  Synthetic Indian Hospital Data", fontsize=14, fontweight="bold")

# Donut
labels = ["Not Readmitted", "Readmitted (30d)"]
sizes  = [total_adm - total_read, total_read]
colors = [PALETTE["not_readmitted"], PALETTE["readmitted"]]
wedges, texts, autotexts = axes[0].pie(
    sizes, labels=labels, colors=colors, autopct="%1.1f%%",
    startangle=90, wedgeprops={"width": 0.55}, textprops={"fontsize": 11}
)
autotexts[1].set_fontweight("bold")
axes[0].set_title(f"30-Day Readmission: {overall_rate:.2f}%")

# Year trend
yearly = admissions.groupby(admissions["admit_date"].dt.year)["readmitted_30d"].mean() * 100
axes[1].plot(yearly.index, yearly.values, marker="o", color=PALETTE["readmitted"], linewidth=2, markersize=7)
axes[1].set_title("Readmission Rate by Year")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Readmission Rate (%)")
axes[1].yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))

plt.tight_layout()
save_fig("overall_readmission.png", fig)


# ============================================================
# 2. READMISSION BY AGE GROUP
# ============================================================

print("[2] Readmission by age group...")

base["age_group"] = pd.cut(
    base["age"],
    bins=[0, 29, 44, 59, 74, 200],
    labels=["18-29", "30-44", "45-59", "60-74", "75+"]
)
age_rates = base.groupby("age_group", observed=True)["readmitted_30d"].mean() * 100

fig, ax = plt.subplots(figsize=(10, 6))
colors = [PALETTE["low"] if v < overall_rate else PALETTE["readmitted"] for v in age_rates.values]
bar_chart(ax, age_rates.index.astype(str), age_rates.values, color=colors)
ax.axhline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall avg {overall_rate:.1f}%")
ax.set_title("30-Day Readmission Rate by Age Group  |  Synthetic Data")
ax.set_xlabel("Age Group")
ax.set_ylabel("Readmission Rate (%)")
ax.legend()
save_fig("readmission_by_age.png", fig)


# ============================================================
# 3. READMISSION BY DIAGNOSIS CATEGORY
# ============================================================

print("[3] Readmission by diagnosis...")

diagnoses = pd.read_csv(CLEAN_DIR / "diagnoses_clean.csv",
                        dtype={"diag_id": str, "admission_id": str})
primary_dx = diagnoses[diagnoses["diag_rank"] == 1][["admission_id", "diag_category"]]
adm_dx = admissions.merge(primary_dx, on="admission_id", how="left")
diag_rates = (
    adm_dx.groupby("diag_category")["readmitted_30d"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "rate", "count": "n"})
)
diag_rates = diag_rates[diag_rates["n"] >= 200].sort_values("rate", ascending=True)
diag_rates["rate_pct"] = diag_rates["rate"] * 100

fig, ax = plt.subplots(figsize=(12, 8))
colors = [PALETTE["readmitted"] if v > overall_rate else PALETTE["not_readmitted"] for v in diag_rates["rate_pct"]]
bars = ax.barh(diag_rates.index, diag_rates["rate_pct"], color=colors, edgecolor="white")
ax.axvline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall {overall_rate:.1f}%")
for bar, val in zip(bars, diag_rates["rate_pct"]):
    ax.text(val + 0.1, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%", va="center", fontsize=9)
ax.set_title("30-Day Readmission Rate by Diagnosis Category  |  Synthetic Data")
ax.set_xlabel("Readmission Rate (%)")
ax.legend()
plt.tight_layout()
save_fig("readmission_by_diagnosis.png", fig)


# ============================================================
# 4. READMISSION BY INSURANCE TYPE
# ============================================================

print("[4] Readmission by insurance...")

ins_rates = base.groupby("insurance_type")["readmitted_30d"].mean() * 100
ins_rates = ins_rates.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(9, 6))
bar_chart(ax, ins_rates.index, ins_rates.values)
ax.axhline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall {overall_rate:.1f}%")
ax.set_title("30-Day Readmission Rate by Insurance Type  |  Synthetic Data")
ax.set_xlabel("Insurance Type")
ax.set_ylabel("Readmission Rate (%)")
ax.legend()
save_fig("readmission_by_insurance.png", fig)


# ============================================================
# 5. READMISSION BY PREVIOUS ADMISSIONS
# ============================================================

print("[5] Readmission by previous admissions...")

prev_rates = base.groupby("prev_admissions")["readmitted_30d"].mean() * 100

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(prev_rates.index, prev_rates.values, marker="o", color=PALETTE["readmitted"], linewidth=2)
ax.fill_between(prev_rates.index, prev_rates.values, alpha=0.15, color=PALETTE["readmitted"])
ax.axhline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall {overall_rate:.1f}%")
ax.set_title("30-Day Readmission Rate by No. of Previous Admissions  |  Synthetic Data")
ax.set_xlabel("Previous Admissions")
ax.set_ylabel("Readmission Rate (%)")
ax.legend()
save_fig("readmission_by_previous_admissions.png", fig)


# ============================================================
# 6. READMISSION BY COMORBIDITY COUNT
# ============================================================

print("[6] Readmission by comorbidity count...")

comor_rates = base.groupby("comorbidity_count")["readmitted_30d"].mean() * 100

fig, ax = plt.subplots(figsize=(10, 6))
bar_chart(ax, comor_rates.index.astype(str), comor_rates.values)
ax.axhline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall {overall_rate:.1f}%")
ax.set_title("30-Day Readmission Rate by Comorbidity Count  |  Synthetic Data")
ax.set_xlabel("Comorbidity Count")
ax.set_ylabel("Readmission Rate (%)")
ax.legend()
save_fig("readmission_by_comorbidity.png", fig)


# ============================================================
# 7. READMISSION BY HOSPITAL
# ============================================================

print("[7] Readmission by hospital...")

hosp_rates = (
    base.groupby(["name"])["readmitted_30d"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "rate", "count": "n"})
)
hosp_rates = hosp_rates[hosp_rates["n"] >= 200].sort_values("rate", ascending=True)
hosp_rates["rate_pct"] = hosp_rates["rate"] * 100

fig, ax = plt.subplots(figsize=(12, 10))
colors = [PALETTE["readmitted"] if v > overall_rate else PALETTE["not_readmitted"] for v in hosp_rates["rate_pct"]]
bars = ax.barh(hosp_rates.index, hosp_rates["rate_pct"], color=colors, edgecolor="white")
ax.axvline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall {overall_rate:.1f}%")
for bar, val in zip(bars, hosp_rates["rate_pct"]):
    ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%", va="center", fontsize=9)
ax.set_title("30-Day Readmission Rate by Hospital  |  Synthetic Data")
ax.set_xlabel("Readmission Rate (%)")
ax.legend()
plt.tight_layout()
save_fig("readmission_by_hospital.png", fig)


# ============================================================
# 8. READMISSION BY STATE
# ============================================================

print("[8] Readmission by state...")

state_rates = base.groupby("state_x")["readmitted_30d"].mean() * 100
state_rates = state_rates.sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(12, 9))
colors = [PALETTE["readmitted"] if v > overall_rate else PALETTE["not_readmitted"] for v in state_rates.values]
bars = ax.barh(state_rates.index, state_rates.values, color=colors, edgecolor="white")
ax.axvline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall {overall_rate:.1f}%")
for bar, val in zip(bars, state_rates.values):
    ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%", va="center", fontsize=9)
ax.set_title("30-Day Readmission Rate by Patient State  |  Synthetic Data")
ax.set_xlabel("Readmission Rate (%)")
ax.legend()
plt.tight_layout()
save_fig("readmission_by_state.png", fig)


# ============================================================
# 9. FINANCIAL IMPACT
# ============================================================

print("[9] Financial impact...")

fin = base.groupby("readmitted_30d")[["total_cost_inr", "govt_subsidy_inr", "out_of_pocket_inr"]].mean()
fin.index = ["Not Readmitted", "Readmitted"]

fig, axes = plt.subplots(1, 3, figsize=(14, 6))
fig.suptitle("Average Financial Metrics by Readmission Status  |  Synthetic Data", fontsize=13, fontweight="bold")

for ax, col, title in zip(axes,
                           ["total_cost_inr", "govt_subsidy_inr", "out_of_pocket_inr"],
                           ["Total Cost (INR)", "Govt Subsidy (INR)", "Out-of-Pocket (INR)"]):
    colors = [PALETTE["not_readmitted"], PALETTE["readmitted"]]
    bars = ax.bar(fin.index, fin[col], color=colors, edgecolor="white")
    for bar, val in zip(bars, fin[col]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                f"₹{val:,.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_title(title)
    ax.set_ylabel("Amount (INR)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))

plt.tight_layout()
save_fig("financial_impact.png", fig)


# ============================================================
# 10. HISTORICAL FOLLOW-UP PRIORITY
# ============================================================

print("[10] Historical follow-up priority segmentation...")

def compute_priority_score(df):
    score = pd.Series(0, index=df.index)
    score += np.where(df["prev_admissions"]   >= 3,           3, 0)
    score += np.where(df["comorbidity_count"] >= 3,           3, 0)
    score += np.where(df["charlson_index"]    >= 3,           3, 0)
    score += np.where(df["age"]               >= 60,          2, 0)
    score += np.where(df["los_days"]          >= 7,           2, 0)
    score += np.where(df["admit_type"]        == "Emergency", 2, 0)
    score += np.where(df["discharge_type"]    == "LAMA",      3, 0)
    score += np.where(df["discharge_type"]    == "Referred",  2, 0)
    score += np.where(df["ward_type"]         == "ICU",       2, 0)
    return score

base["priority_score"]  = compute_priority_score(base)
base["followup_priority"] = pd.cut(
    base["priority_score"],
    bins=[-1, 4, 9, 100],
    labels=["LOW", "MEDIUM", "HIGH"]
)

priority_summary = (
    base.groupby("followup_priority", observed=True)["readmitted_30d"]
    .agg(["count", "sum", "mean"])
    .rename(columns={"count": "admissions", "sum": "readmissions", "mean": "rate"})
)
priority_summary["rate_pct"] = priority_summary["rate"] * 100

print("\n  Historical Follow-Up Priority Summary:")
print(priority_summary[["admissions", "readmissions", "rate_pct"]].to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle(
    "Historical Follow-Up Priority  |  Synthetic Data\n"
    "Not a clinical diagnosis — based on historical dataset patterns only",
    fontsize=12, fontweight="bold"
)

# Count distribution
tier_colors = [PALETTE["low"], PALETTE["medium"], PALETTE["high"]]
axes[0].bar(priority_summary.index.astype(str), priority_summary["admissions"],
            color=tier_colors, edgecolor="white")
for i, (idx, row) in enumerate(priority_summary.iterrows()):
    axes[0].text(i, row["admissions"] + 200, f"{row['admissions']:,}", ha="center", fontsize=10)
axes[0].set_title("Admissions by Priority Tier")
axes[0].set_xlabel("Historical Follow-Up Priority")
axes[0].set_ylabel("Number of Admissions")

# Readmission rate by tier
axes[1].bar(priority_summary.index.astype(str), priority_summary["rate_pct"],
            color=tier_colors, edgecolor="white")
axes[1].axhline(overall_rate, color="gray", linestyle="--", linewidth=1, label=f"Overall {overall_rate:.1f}%")
for i, (idx, row) in enumerate(priority_summary.iterrows()):
    axes[1].text(i, row["rate_pct"] + 0.2, f"{row['rate_pct']:.1f}%", ha="center", fontsize=10, fontweight="bold")
axes[1].set_title("Readmission Rate by Priority Tier")
axes[1].set_xlabel("Historical Follow-Up Priority")
axes[1].set_ylabel("Readmission Rate (%)")
axes[1].legend()

plt.tight_layout()
save_fig("followup_priority.png", fig)


# ============================================================
# SUMMARY REPORT
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print(f"\nOverall readmission rate  : {overall_rate:.2f}%")
print(f"Total admissions          : {total_adm:,}")
print(f"Total readmissions (30d)  : {int(total_read):,}")
print(f"Average LOS               : {avg_los:.1f} days")
print(f"\nCharts saved to: python/output/")
print("\nDISCLAIMER: All results are derived from synthetic data")
print("and are for portfolio/analytical purposes only.")
print("=" * 60)
