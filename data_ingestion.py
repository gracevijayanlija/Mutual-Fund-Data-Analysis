"""
===============================================================
  Mutual Fund Analytics — Day 1: Complete Data Ingestion
  Uses 10 provided CSV datasets + live NAV from mfapi.in
===============================================================
"""

import os
import time
import requests
import pandas as pd
from datetime import datetime

# ── 1. CREATE FOLDER STRUCTURE ─────────────────────────────────
FOLDERS = ["data/raw","data/processed","notebooks","sql","dashboard","reports"]

print("=" * 60)
print("  STEP 1: Creating project folder structure")
print("=" * 60)
for folder in FOLDERS:
    os.makedirs(folder, exist_ok=True)
    print(f"  ✓ Created/Verified: {folder}/")

# ── 2. LOAD ALL 10 PROVIDED CSV DATASETS ──────────────────────
print("\n" + "=" * 60)
print("  STEP 2: Loading all 10 provided CSV datasets")
print("=" * 60)

DATASET_FILES = {
    "fund_master":           "data/raw/01_fund_master.csv",
    "nav_history":           "data/raw/02_nav_history.csv",
    "aum_by_fund_house":     "data/raw/03_aum_by_fund_house.csv",
    "monthly_sip_inflows":   "data/raw/04_monthly_sip_inflows.csv",
    "category_inflows":      "data/raw/05_category_inflows.csv",
    "industry_folio_count":  "data/raw/06_industry_folio_count.csv",
    "scheme_performance":    "data/raw/07_scheme_performance.csv",
    "investor_transactions": "data/raw/08_investor_transactions.csv",
    "portfolio_holdings":    "data/raw/09_portfolio_holdings.csv",
    "benchmark_indices":     "data/raw/10_benchmark_indices.csv",
}

datasets  = {}
anomalies = []

for name, path in DATASET_FILES.items():
    print(f"\n{'─'*55}")
    print(f" Dataset : {name}")
    print(f"{'─'*55}")

    if not os.path.exists(path):
        print(f"  ✗ FILE NOT FOUND — copy {os.path.basename(path)} into data/raw/")
        anomalies.append(f"{name}: file not found")
        continue

    try:
        df = pd.read_csv(path)
        datasets[name] = df

        print(f"  Shape   : {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"\n  dtypes:\n{df.dtypes.to_string()}")
        print(f"\n  head(3):\n{df.head(3).to_string()}")

        notes = []
        null_counts = df.isnull().sum()
        nulls = null_counts[null_counts > 0]
        if not nulls.empty:
            notes.append(f"Nulls in: {nulls.to_dict()}")
        if "amfi_code" in df.columns and name in ("fund_master", "scheme_performance"):
            dups = df["amfi_code"].duplicated().sum()
            if dups:
                notes.append(f"{dups} duplicate amfi_codes")
        if "nav" in df.columns:
            bad_nav = pd.to_numeric(df["nav"], errors="coerce").isna().sum()
            if bad_nav:
                notes.append(f"{bad_nav} non-numeric NAV values")

        if notes:
            for note in notes:
                print(f"\n  ⚠️  {note}")
                anomalies.append(f"{name}: {note}")
        else:
            print(f"\n No anomalies detected")

    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        anomalies.append(f"{name}: read error — {e}")

# ── 3. EXPLORE FUND MASTER ────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 3: Fund Master — Unique values exploration")
print("=" * 60)

if "fund_master" in datasets:
    fm = datasets["fund_master"]
    print(f"\n  Fund Houses ({fm['fund_house'].nunique()} unique):")
    for fh in sorted(fm["fund_house"].unique()):
        print(f"    • {fh}")
    print(f"\n  Categories ({fm['category'].nunique()} unique):")
    for cat in sorted(fm["category"].unique()):
        print(f"    • {cat}")
    print(f"\n  Sub-Categories ({fm['sub_category'].nunique()} unique):")
    for sc in sorted(fm["sub_category"].unique()):
        print(f"    • {sc}")
    print(f"\n  Risk Grades:")
    for rg in sorted(fm["risk_category"].unique()):
        count = (fm["risk_category"] == rg).sum()
        print(f"    • {rg:<12} → {count} schemes")
    print(f"\n  AMFI Code range: {fm['amfi_code'].min()} – {fm['amfi_code'].max()}")

# ── 4. VALIDATE AMFI CODES ────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 4: AMFI Code Validation")
print("=" * 60)

matched = set()
only_in_master = set()
only_in_nav = set()

if "fund_master" in datasets and "nav_history" in datasets:
    fm_codes  = set(datasets["fund_master"]["amfi_code"].astype(str))
    nav_codes = set(datasets["nav_history"]["amfi_code"].astype(str))
    only_in_master = fm_codes - nav_codes
    only_in_nav    = nav_codes - fm_codes
    matched        = fm_codes & nav_codes
    print(f"  Fund master codes  : {len(fm_codes):,}")
    print(f"  NAV history codes  : {len(nav_codes):,}")
    print(f"  ✓ Matched          : {len(matched):,}")
    if only_in_master:
        print(f" Master only     : {sorted(only_in_master)}")
        anomalies.append(f"AMFI: {len(only_in_master)} codes in master but not nav_history")
    if only_in_nav:
        print(f" NAV only        : {sorted(only_in_nav)}")
        anomalies.append(f"AMFI: {len(only_in_nav)} codes in nav_history but not master")
    if not only_in_master and not only_in_nav:
        print(f" All codes match perfectly!")

# ── 5. FETCH LIVE NAV ─────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 5: Fetching live NAV from mfapi.in")
print("=" * 60)

LIVE_SCHEMES = {
    "SBI Bluechip Direct":       119551,
    "ICICI Pru Bluechip Direct": 120503,
    "Nippon Large Cap Direct":   118632,
    "Axis Bluechip Direct":      119092,
    "Kotak Bluechip Direct":     120841,
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
live_results = []

for name, code in LIVE_SCHEMES.items():
    try:
        r    = requests.get(f"https://api.mfapi.in/mf/{code}", headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        latest = data["data"][0]
        meta   = data.get("meta", {})
        live_results.append({
            "scheme_name": name, "amfi_code": code,
            "api_name":    meta.get("scheme_name", "N/A"),
            "fund_house":  meta.get("fund_house", "N/A"),
            "nav":         float(latest["nav"]),
            "nav_date":    latest["date"],
            "fetched_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        print(f"  ✓ {name:<30} NAV: ₹{float(latest['nav']):>10.4f}  ({latest['date']})")
        time.sleep(0.5)
    except Exception as e:
        print(f"  ✗ {name:<30} ERROR: {e}")

if live_results:
    pd.DataFrame(live_results).to_csv("data/raw/live_nav_fetched.csv", index=False)
    print(f"\n  ✓ Saved: data/raw/live_nav_fetched.csv")

# ── 6. DATA QUALITY REPORT ────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 6: Writing data quality report")
print("=" * 60)

lines = [
    "DATA QUALITY REPORT — Mutual Fund Analytics Day 1",
    f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "=" * 55, "",
    "DATASETS LOADED",
]
for name, path in DATASET_FILES.items():
    if name in datasets:
        df = datasets[name]
        status = f"{df.shape[0]:,} rows × {df.shape[1]} cols"
    else:
        status = "NOT LOADED ✗"
    lines.append(f"  {name:<25} → {status}")

lines += ["", "AMFI CODE VALIDATION",
          f"  Matched       : {len(matched):,}",
          f"  Master only   : {len(only_in_master)}",
          f"  NAV only      : {len(only_in_nav)}",
          f"  Result        : {'PERFECT MATCH' if not only_in_master and not only_in_nav else 'Mismatches found'}",
          "", "ANOMALIES"]
lines += [f"  - {a}" for a in anomalies] if anomalies else ["  None detected."]

lines += ["", "LIVE NAV SNAPSHOT"]
if live_results:
    for r in live_results:
        lines.append(f"  {r['scheme_name']:<30} ₹{r['nav']:>10.4f}  ({r['nav_date']})")
else:
    lines.append("  API unavailable during run.")

report_text = "\n".join(lines) + "\n"
with open("reports/data_quality_day1.txt", "w") as f:
    f.write(report_text)

print(report_text)
print("  ✓ Saved: reports/data_quality_day1.txt")

print("\n" + "=" * 60)
print(f"ALL DONE!  {len(datasets)}/10 datasets loaded.")
print("=" * 60 + "\n")
