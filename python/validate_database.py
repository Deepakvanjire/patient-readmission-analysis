"""
============================================================
PATIENT READMISSION ANALYSIS
Database Validation Script
============================================================
Runs comprehensive SQL checks against the MySQL database
and prints a structured validation report.

Usage:
    python validate_database.py
============================================================
"""

import os
import sys
from pathlib import Path
from datetime import datetime

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST",     "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", "3306")),
    "user":     os.getenv("MYSQL_USER",     "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "patient_readmission"),
}

EXPECTED_COUNTS = {
    "patients":   86_400,
    "hospitals":  33,
    "admissions": 120_000,
    "diagnoses":  271_341,
    "billing":    120_000,
}

PASS = "  [PASS]"
FAIL = "  [FAIL]"
INFO = "  [INFO]"

issues = []


def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[ERROR] Cannot connect to MySQL: {e}")
        sys.exit(1)


def run_query(cursor, sql):
    cursor.execute(sql)
    return cursor.fetchall()


def check(label, condition, detail=""):
    if condition:
        print(f"{PASS} {label}  {detail}")
    else:
        print(f"{FAIL} {label}  {detail}")
        issues.append(f"{label}: {detail}")


def section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


def check_row_counts(cursor):
    section("A. ROW COUNTS")
    for table, expected in EXPECTED_COUNTS.items():
        rows = run_query(cursor, f"SELECT COUNT(*) FROM `{table}`")[0][0]
        check(f"{table} row count", rows == expected, f"expected={expected:,}  actual={rows:,}")


def check_duplicate_pks(cursor):
    section("B. DUPLICATE PRIMARY KEYS")
    checks = [
        ("patients",   "patient_id"),
        ("admissions", "admission_id"),
        ("hospitals",  "hospital_id"),
        ("diagnoses",  "diag_id"),
        ("billing",    "bill_id"),
    ]
    for table, pk in checks:
        sql = f"SELECT COUNT(*) FROM (SELECT `{pk}`, COUNT(*) AS cnt FROM `{table}` GROUP BY `{pk}` HAVING cnt > 1) t"
        dupes = run_query(cursor, sql)[0][0]
        check(f"No duplicate {pk} in {table}", dupes == 0, f"duplicates={dupes}")


def check_foreign_keys(cursor):
    section("C. FOREIGN KEY INTEGRITY")
    fk_checks = [
        ("Admissions -> Patients",  "SELECT COUNT(*) FROM admissions a LEFT JOIN patients p ON a.patient_id = p.patient_id WHERE p.patient_id IS NULL"),
        ("Admissions -> Hospitals", "SELECT COUNT(*) FROM admissions a LEFT JOIN hospitals h ON a.hospital_id = h.hospital_id WHERE h.hospital_id IS NULL"),
        ("Diagnoses -> Admissions", "SELECT COUNT(*) FROM diagnoses d LEFT JOIN admissions a ON d.admission_id = a.admission_id WHERE a.admission_id IS NULL"),
        ("Billing -> Admissions",   "SELECT COUNT(*) FROM billing b LEFT JOIN admissions a ON b.admission_id = a.admission_id WHERE a.admission_id IS NULL"),
    ]
    for label, sql in fk_checks:
        broken = run_query(cursor, sql)[0][0]
        check(label, broken == 0, f"broken_refs={broken}")


def check_null_values(cursor):
    section("D. NULL VALUE CHECKS (critical columns)")
    null_checks = [
        ("patients",   ["patient_id", "age", "gender", "state", "insurance_type"]),
        ("admissions", ["admission_id", "patient_id", "admit_date", "discharge_date", "los_days", "readmitted_30d"]),
        ("hospitals",  ["hospital_id", "name", "state", "tier"]),
        ("diagnoses",  ["diag_id", "admission_id", "icd10_code", "diag_category"]),
        ("billing",    ["bill_id", "admission_id", "total_cost_inr"]),
    ]
    for table, cols in null_checks:
        for col in cols:
            nulls = run_query(cursor, f"SELECT COUNT(*) FROM `{table}` WHERE `{col}` IS NULL")[0][0]
            check(f"No NULLs in {table}.{col}", nulls == 0, f"nulls={nulls}")


def check_dates(cursor):
    section("E. DATE VALIDITY")
    bad = run_query(cursor, "SELECT COUNT(*) FROM admissions WHERE admit_date > discharge_date")[0][0]
    check("admit_date <= discharge_date for all rows", bad == 0, f"bad_rows={bad}")
    row = run_query(cursor, "SELECT MIN(admit_date), MAX(admit_date) FROM admissions")[0]
    print(f"{INFO} admit_date range: {row[0]}  to  {row[1]}")
    bad2 = run_query(cursor, "SELECT COUNT(*) FROM admissions WHERE admit_date < '2000-01-01' OR admit_date > '2030-12-31'")[0][0]
    check("admit_date within plausible range (2000-2030)", bad2 == 0, f"bad_rows={bad2}")


def check_numeric_ranges(cursor):
    section("F. NUMERIC RANGE CHECKS")
    checks = [
        ("patients.age",              "SELECT MIN(age), MAX(age) FROM patients",                              0,   130),
        ("admissions.los_days",       "SELECT MIN(los_days), MAX(los_days) FROM admissions",                  0,   365),
        ("admissions.charlson_index", "SELECT MIN(charlson_index), MAX(charlson_index) FROM admissions",      0,    50),
        ("billing.total_cost_inr",    "SELECT MIN(total_cost_inr), MAX(total_cost_inr) FROM billing",         0, 10_000_000),
    ]
    for label, sql, lo, hi in checks:
        mn, mx = run_query(cursor, sql)[0]
        ok = (mn is not None) and (mx is not None) and (float(mn) >= lo) and (float(mx) <= hi)
        print(f"{INFO} {label}: min={mn}  max={mx}")
        check(f"{label} within [{lo}, {hi}]", ok)


def check_readmission_distribution(cursor):
    section("G. READMISSION DISTRIBUTION")
    rows = run_query(cursor, "SELECT readmitted_30d, COUNT(*) AS cnt FROM admissions GROUP BY readmitted_30d ORDER BY readmitted_30d")
    total = sum(r[1] for r in rows)
    readmitted = 0
    for val, cnt in rows:
        pct = cnt / total * 100 if total else 0
        print(f"{INFO} readmitted_30d={val}: {cnt:,} ({pct:.2f}%)")
        if val == 1:
            readmitted = cnt
    rate = readmitted / total * 100 if total else 0
    check("30-day readmission rate plausible (10-14%)", 10.0 <= rate <= 14.0, f"rate={rate:.2f}%")


def check_insurance_distribution(cursor):
    section("H. INSURANCE TYPE DISTRIBUTION")
    rows = run_query(cursor, "SELECT insurance_type, COUNT(*) AS cnt FROM patients GROUP BY insurance_type ORDER BY cnt DESC")
    for ins_type, cnt in rows:
        print(f"{INFO} {ins_type:<15} {cnt:,}")
    types = {r[0] for r in rows}
    check("insurance_type includes 'Unknown'",  "Unknown"  in types)
    check("insurance_type includes 'Ayushman'", "Ayushman" in types)


def check_diagnosis_relationships(cursor):
    section("I. DIAGNOSIS RELATIONSHIPS")
    distinct = run_query(cursor, "SELECT COUNT(DISTINCT admission_id) FROM diagnoses")[0][0]
    print(f"{INFO} Distinct admissions with diagnoses: {distinct:,}")
    mn, mx = run_query(cursor, "SELECT MIN(diag_rank), MAX(diag_rank) FROM diagnoses")[0]
    print(f"{INFO} diag_rank range: {mn} - {mx}")
    check("diag_rank >= 1 for all rows", mn is not None and int(mn) >= 1, f"min={mn}")


def check_billing_relationships(cursor):
    section("J. BILLING RELATIONSHIPS")
    mn, mx, avg = run_query(cursor, "SELECT MIN(total_cost_inr), MAX(total_cost_inr), AVG(total_cost_inr) FROM billing")[0]
    print(f"{INFO} total_cost_inr: min={mn:,.0f}  max={mx:,.0f}  avg={float(avg):,.0f}")
    bad = run_query(cursor, "SELECT COUNT(*) FROM billing WHERE total_cost_inr <= 0")[0][0]
    check("total_cost_inr > 0 for all rows", bad == 0, f"bad_rows={bad}")
    bad2 = run_query(cursor, "SELECT COUNT(*) FROM billing WHERE out_of_pocket_inr < 0")[0][0]
    check("No negative out_of_pocket_inr", bad2 == 0, f"bad_rows={bad2}")


def main():
    print("\n" + "=" * 55)
    print("  PATIENT READMISSION - Database Validation Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    conn = connect_db()
    cursor = conn.cursor()
    print(f"\n[INFO] Connected to {DB_CONFIG['host']}:{DB_CONFIG['port']} / {DB_CONFIG['database']}")

    check_row_counts(cursor)
    check_duplicate_pks(cursor)
    check_foreign_keys(cursor)
    check_null_values(cursor)
    check_dates(cursor)
    check_numeric_ranges(cursor)
    check_readmission_distribution(cursor)
    check_insurance_distribution(cursor)
    check_diagnosis_relationships(cursor)
    check_billing_relationships(cursor)

    cursor.close()
    conn.close()

    section("VALIDATION SUMMARY")
    if not issues:
        print(f"{PASS} ALL CHECKS PASSED - database is clean and complete.\n")
    else:
        print(f"  {len(issues)} issue(s) found:\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()


if __name__ == "__main__":
    main()
