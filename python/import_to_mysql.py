"""
============================================================
PATIENT READMISSION ANALYSIS
MySQL Import Script
============================================================
Reads cleaned CSVs and imports them into MySQL in dependency
order using chunked batch inserts.

Usage:
    python import_to_mysql.py

Requires .env file in the project root with:
    MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
============================================================
"""

import os
import sys
import math
from pathlib import Path

import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "cleaned_data"

# Load .env from project root
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST",     "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", "3306")),
    "user":     os.getenv("MYSQL_USER",     "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "patient_readmission"),
    "allow_local_infile": True,
}

CHUNK_SIZE = 5000   # rows per batch insert

EXPECTED_COUNTS = {
    "patients":   86_400,
    "hospitals":  33,
    "admissions": 120_000,
    "diagnoses":  271_341,
    "billing":    120_000,
}

# ============================================================
# HELPERS
# ============================================================

def connect_db():
    """Return a MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"\n[ERROR] Cannot connect to MySQL: {e}")
        sys.exit(1)


def get_row_count(cursor, table):
    cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
    return cursor.fetchone()[0]


def clear_tables(conn):
    """
    Safely clear only the five project tables.
    Uses FK-check bypass so child rows are deleted before parents.
    Does NOT touch any other database.
    """
    cursor = conn.cursor()
    print("\n[INFO] Clearing existing project table data...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for tbl in ["diagnoses", "billing", "admissions", "patients", "hospitals"]:
        cursor.execute(f"DELETE FROM `{tbl}`")
        print(f"  OK  {tbl} cleared")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    cursor.close()
    print("[INFO] All project tables cleared.\n")


def insert_chunked(conn, table, df, columns, placeholders):
    """
    Insert a DataFrame into a table in chunks.
    Returns total rows inserted or raises on error.
    """
    cursor = conn.cursor()
    sql = (
        f"INSERT INTO `{table}` ({columns}) "
        f"VALUES ({placeholders})"
    )
    total = len(df)
    n_chunks = math.ceil(total / CHUNK_SIZE)
    inserted = 0

    for i in range(n_chunks):
        chunk = df.iloc[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
        data = [tuple(row) for row in chunk.itertuples(index=False, name=None)]
        cursor.executemany(sql, data)
        conn.commit()
        inserted += len(data)
        pct = inserted / total * 100
        print(f"  {table}: {inserted:>7,} / {total:,}  ({pct:.1f}%)", end="\r")

    cursor.close()
    print(f"  {table}: {inserted:,} rows inserted.               ")
    return inserted


# ============================================================
# TABLE IMPORT FUNCTIONS
# ============================================================

def import_patients(conn):
    print("[1/5] Importing PATIENTS ...")
    df = pd.read_csv(
        CLEAN_DIR / "patients_clean.csv",
        dtype={
            "patient_id":        str,
            "gender":            str,
            "state":             str,
            "bpl_card":          str,
            "insurance_type":    str,
        }
    )
    df = df.where(pd.notnull(df), None)
    cols = "patient_id, age, gender, state, bpl_card, insurance_type, comorbidity_count, prev_admissions"
    ph   = "%s, %s, %s, %s, %s, %s, %s, %s"
    col_order = ["patient_id","age","gender","state","bpl_card","insurance_type","comorbidity_count","prev_admissions"]
    return insert_chunked(conn, "patients", df[col_order], cols, ph)


def import_hospitals(conn):
    print("[2/5] Importing HOSPITALS ...")
    df = pd.read_csv(
        CLEAN_DIR / "hospitals_clean.csv",
        dtype={
            "hospital_id": str,
            "name":        str,
            "state":       str,
            "tier":        str,
            "teaching":    str,
        }
    )
    df = df.where(pd.notnull(df), None)
    cols = "hospital_id, name, state, tier, beds, teaching"
    ph   = "%s, %s, %s, %s, %s, %s"
    col_order = ["hospital_id","name","state","tier","beds","teaching"]
    return insert_chunked(conn, "hospitals", df[col_order], cols, ph)


def import_admissions(conn):
    print("[3/5] Importing ADMISSIONS ...")
    df = pd.read_csv(
        CLEAN_DIR / "admissions_clean.csv",
        dtype={
            "admission_id":   str,
            "patient_id":     str,
            "hospital_id":    str,
            "admit_type":     str,
            "ward_type":      str,
            "discharge_type": str,
        },
        parse_dates=["admit_date", "discharge_date"],
    )
    df["admit_date"]     = df["admit_date"].dt.strftime("%Y-%m-%d")
    df["discharge_date"] = df["discharge_date"].dt.strftime("%Y-%m-%d")
    df = df.where(pd.notnull(df), None)
    cols = (
        "admission_id, patient_id, admit_date, discharge_date, los_days, "
        "admit_type, ward_type, hospital_id, discharge_type, num_procedures, "
        "charlson_index, hba1c, creatinine, haemoglobin, systolic_bp, "
        "readmitted_30d, readmitted_7d"
    )
    ph = ", ".join(["%s"] * 17)
    col_order = [
        "admission_id","patient_id","admit_date","discharge_date","los_days",
        "admit_type","ward_type","hospital_id","discharge_type","num_procedures",
        "charlson_index","hba1c","creatinine","haemoglobin","systolic_bp",
        "readmitted_30d","readmitted_7d"
    ]
    return insert_chunked(conn, "admissions", df[col_order], cols, ph)


def import_diagnoses(conn):
    print("[4/5] Importing DIAGNOSES (chunked file read) ...")
    cursor = conn.cursor()
    sql = (
        "INSERT INTO `diagnoses` "
        "(diag_id, admission_id, icd10_code, diag_desc, diag_rank, diag_category) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    total_inserted = 0

    for chunk in pd.read_csv(
        CLEAN_DIR / "diagnoses_clean.csv",
        dtype={
            "diag_id":       str,
            "admission_id":  str,
            "icd10_code":    str,
            "diag_desc":     str,
            "diag_category": str,
        },
        chunksize=CHUNK_SIZE,
    ):
        chunk = chunk.where(pd.notnull(chunk), None)
        col_order = ["diag_id","admission_id","icd10_code","diag_desc","diag_rank","diag_category"]
        data = [tuple(row) for row in chunk[col_order].itertuples(index=False, name=None)]
        cursor.executemany(sql, data)
        conn.commit()
        total_inserted += len(data)
        pct = total_inserted / 271_341 * 100
        print(f"  diagnoses: {total_inserted:>7,} / 271,341  ({pct:.1f}%)", end="\r")

    cursor.close()
    print(f"  diagnoses: {total_inserted:,} rows inserted.               ")
    return total_inserted


def import_billing(conn):
    print("[5/5] Importing BILLING ...")
    df = pd.read_csv(
        CLEAN_DIR / "billing_clean.csv",
        dtype={
            "bill_id":       str,
            "admission_id":  str,
            "cost_category": str,
        }
    )
    df = df.where(pd.notnull(df), None)
    cols = "bill_id, admission_id, total_cost_inr, govt_subsidy_inr, out_of_pocket_inr, cost_category"
    ph   = "%s, %s, %s, %s, %s, %s"
    col_order = ["bill_id","admission_id","total_cost_inr","govt_subsidy_inr","out_of_pocket_inr","cost_category"]
    return insert_chunked(conn, "billing", df[col_order], cols, ph)


# ============================================================
# VALIDATION
# ============================================================

def validate_counts(conn):
    cursor = conn.cursor()
    print("\n" + "=" * 50)
    print("POST-IMPORT ROW COUNT VALIDATION")
    print("=" * 50)
    all_ok = True
    for table, expected in EXPECTED_COUNTS.items():
        actual = get_row_count(cursor, table)
        status = "OK" if actual == expected else "MISMATCH"
        print(f"  {table:<12} expected={expected:>7,}  actual={actual:>7,}  [{status}]")
        if actual != expected:
            all_ok = False
    cursor.close()
    return all_ok


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 50)
    print("PATIENT READMISSION - MySQL Import")
    print("=" * 50)

    conn = connect_db()
    print(f"\n[INFO] Connected to MySQL at {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"[INFO] Database: {DB_CONFIG['database']}")

    # Show current counts before clearing
    cursor = conn.cursor()
    print("\n[INFO] Current row counts before import:")
    for tbl in ["patients","hospitals","admissions","diagnoses","billing"]:
        cnt = get_row_count(cursor, tbl)
        print(f"  {tbl:<12} {cnt:,}")
    cursor.close()

    # Clear partial data
    clear_tables(conn)

    # Import in FK-safe dependency order
    try:
        import_patients(conn)
        import_hospitals(conn)
        import_admissions(conn)
        import_diagnoses(conn)
        import_billing(conn)
    except Error as e:
        print(f"\n[ERROR] Import failed: {e}")
        print("[INFO] Rolling back...")
        conn.rollback()
        conn.close()
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        conn.rollback()
        conn.close()
        sys.exit(1)

    # Validate
    ok = validate_counts(conn)
    conn.close()

    print("\n" + "=" * 50)
    if ok:
        print("MYSQL IMPORT COMPLETE")
        print("=" * 50)
        print(f"\n  patients:    86,400")
        print(f"  hospitals:       33")
        print(f"  admissions: 120,000")
        print(f"  diagnoses:  271,341")
        print(f"  billing:    120,000")
        print("\n  All expected records loaded successfully.")
    else:
        print("IMPORT COMPLETED WITH WARNINGS - Row counts mismatch above.")
    print("=" * 50)


if __name__ == "__main__":
    main()
