# Day 2 — Load all cleaned CSV data into SQLite database

import pandas as pd
import sqlite3
import os

# ── 1. CONNECT TO DATABASE ────────────────────────────────────────
conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()
print("Connected to bluestock_mf.db")

# ── 2. LOAD dim_fund ──────────────────────────────────────────────
# Source: fund_master.csv — contains fund name, category, fund house
print("\n Loading dim_fund...")
df_fund = pd.read_csv("data/processed/01_fund_master.csv")
print(f"Columns found: {list(df_fund.columns)}")
print(f"Rows: {len(df_fund)}")

# Rename columns to match our database schema
# We'll map whatever columns exist to what our table expects
df_fund.to_sql("dim_fund", conn, if_exists="replace", index=False)
print("dim_fund loaded")

# ── 3. LOAD dim_date ──────────────────────────────────────────────
# We build dim_date from all unique dates in nav_history
print("\n Building dim_date from nav dates...")
df_nav_dates = pd.read_csv("data/processed/02_nav_history_clean.csv")
df_nav_dates['date'] = pd.to_datetime(df_nav_dates['date'], dayfirst=True, errors='coerce')

# Get all unique dates
unique_dates = sorted(df_nav_dates['date'].dropna().unique())

# Build dim_date table
dim_date_rows = []
for d in unique_dates:
    import pandas as pd
    ts = pd.Timestamp(d)
    dim_date_rows.append({
        'full_date'  : ts.strftime('%Y-%m-%d'),
        'day'        : ts.day,
        'month'      : ts.month,
        'year'       : ts.year,
        'quarter'    : ts.quarter,
        'day_of_week': ts.strftime('%A')
    })

df_date = pd.DataFrame(dim_date_rows)
df_date.to_sql("dim_date", conn, if_exists="replace", index=False)
print(f"Rows: {len(df_date)}")
print("dim_date loaded")

# ── 4. LOAD fact_nav ──────────────────────────────────────────────
print("\n Loading fact_nav...")
df_nav = pd.read_csv("data/processed/02_nav_history_clean.csv")
# Convert date from DD-MM-YYYY to YYYY-MM-DD
df_nav['date'] = pd.to_datetime(df_nav['date'], dayfirst=True)
df_nav['date'] = df_nav['date'].dt.strftime('%Y-%m-%d')

print(f"Rows: {len(df_nav)}")
df_nav.to_sql("fact_nav", conn, if_exists="replace", index=False)
print(" fact_nav loaded")

# ── 5. LOAD fact_transactions ─────────────────────────────────────
print("\n Loading fact_transactions...")
df_trans = pd.read_csv("data/processed/08_investor_transactions_clean.csv")
# Convert date from DD-MM-YYYY to YYYY-MM-DD
df_trans['transaction_date'] = pd.to_datetime(df_trans['transaction_date'], dayfirst=True)
df_trans['transaction_date'] = df_trans['transaction_date'].dt.strftime('%Y-%m-%d')

print(f"   Rows: {len(df_trans)}")
df_trans.to_sql("fact_transactions", conn, if_exists="replace", index=False)
print("   ✅ fact_transactions loaded")

# ── 6. LOAD fact_performance ──────────────────────────────────────
print("\n Loading fact_performance...")
df_perf = pd.read_csv("data/processed/07_scheme_performance_clean.csv")
print(f"Columns found: {list(df_perf.columns)}")
print(f"Rows: {len(df_perf)}")
df_perf.to_sql("fact_performance", conn, if_exists="replace", index=False)
print("fact_performance loaded")

# ── 7. LOAD fact_aum ──────────────────────────────────────────────
print("\n Loading fact_aum...")
df_aum = pd.read_csv("data/processed/03_aum_by_fund_house.csv")
print(f"Columns found: {list(df_aum.columns)}")
print(f"Rows: {len(df_aum)}")
df_aum.to_sql("fact_aum", conn, if_exists="replace", index=False)
print("fact_aum loaded")

# ── 8. LOAD REMAINING SUPPORTING TABLES ──────────────────────────
print("\n Loading supporting tables...")

df_sip = pd.read_csv("data/processed/04_monthly_sip_inflows.csv")
df_sip.to_sql("sip_inflows", conn, if_exists="replace", index=False)
print(f"sip_inflows loaded — {len(df_sip)} rows")

df_cat = pd.read_csv("data/processed/05_category_inflows.csv")
df_cat.to_sql("category_inflows", conn, if_exists="replace", index=False)
print(f"category_inflows loaded — {len(df_cat)} rows")

df_folio = pd.read_csv("data/processed/06_industry_folio_count.csv")
df_folio.to_sql("folio_count", conn, if_exists="replace", index=False)
print(f"folio_count loaded — {len(df_folio)} rows")

df_holdings = pd.read_csv("data/processed/09_portfolio_holdings.csv")
df_holdings.to_sql("portfolio_holdings", conn, if_exists="replace", index=False)
print(f"portfolio_holdings loaded — {len(df_holdings)} rows")

df_bench = pd.read_csv("data/processed/10_benchmark_indices.csv")
df_bench.to_sql("benchmark_indices", conn, if_exists="replace", index=False)
print(f"benchmark_indices loaded — {len(df_bench)} rows")

# ── 9. VERIFY EVERYTHING ──────────────────────────────────────────
print("\n" + "="*50)
print("FINAL VERIFICATION — ALL TABLES IN DATABASE")
print("="*50)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"{table[0]:<30} {count:>8} rows")

conn.commit()
conn.close()
print("\n All data loaded successfully into bluestock_mf.db!")