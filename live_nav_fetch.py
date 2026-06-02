"""
===============================================================
  Mutual Fund Analytics — Live NAV Fetcher
  Fetches current NAV for 5 key schemes from mfapi.in
===============================================================
"""

import requests
import pandas as pd
from datetime import datetime

# ── 5 KEY SCHEMES ──────────
SCHEMES = {
    "SBI Bluechip Fund - Regular Plan - Growth":          119551,
    "ICICI Pru Bluechip Fund - Regular - Growth":         120503,
    "Nippon India Large Cap Fund - Regular - Growth":     118632,
    "Axis Bluechip Fund - Regular - Growth":              119092,
    "Kotak Bluechip Fund - Regular - Growth":             120841,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ── FETCH LIVE NAV ─────────────────────────────────────────────
print("=" * 60)
print("  Live NAV Fetch — mfapi.in")
print(f"  Fetched at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

results = []

for name, code in SCHEMES.items():
    url = f"https://api.mfapi.in/mf/{code}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()

        latest     = data["data"][0]
        meta       = data.get("meta", {})
        nav        = float(latest["nav"])
        nav_date   = latest["date"]
        prev_nav   = float(data["data"][1]["nav"]) if len(data["data"]) > 1 else nav
        change     = nav - prev_nav
        change_pct = (change / prev_nav) * 100

        results.append({
            "amfi_code":   code,
            "scheme_name": name,
            "nav":         nav,
            "nav_date":    nav_date,
            "prev_nav":    prev_nav,
            "change":      round(change, 4),
            "change_pct":  round(change_pct, 2),
            "fetched_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        arrow = "▲" if change >= 0 else "▼"
        print(f"  ✓ {name:<50} ₹{nav:>10.4f}  {arrow}{change_pct:+.2f}%  ({nav_date})")

    except requests.RequestException as e:
        print(f"  ✗ {name:<50} ERROR: {e}")
        results.append({
            "amfi_code": code, "scheme_name": name,
            "nav": None, "nav_date": None, "error": str(e)
        })

# ── SAVE TO CSV ────────────────────────────────────────────────
df = pd.DataFrame(results)
timestamp   = datetime.now().strftime("%Y%m%d_%H%M")
output_path = f"data/raw/live_nav_{timestamp}.csv"
df.to_csv(output_path, index=False)

# ── SUMMARY TABLE ──────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"  {'Scheme':<50} {'NAV':>10}  {'Change':>9}  Date")
print(f"  {'─'*50} {'─'*10}  {'─'*9}  {'─'*12}")
for _, row in df.iterrows():
    if row.get("nav"):
        arrow = "▲" if row["change"] >= 0 else "▼"
        print(f"  {row['scheme_name']:<50} ₹{row['nav']:>9.4f}"
              f"  {arrow}{abs(row['change_pct']):>7.2f}%  {row['nav_date']}")

print(f"\n Saved to: {output_path}")
print("=" * 60 + "\n")
