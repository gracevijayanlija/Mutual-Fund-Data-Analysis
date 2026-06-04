# Mutual Fund Analytics — Data Dictionary
**Project:** Bluestock Fintech Internship  
**Author:** Grace Vijayan Lija
**Created:** Day 2 — Data Cleaning & Database Design  
**Database:** bluestock_mf.db  

---

## Table of Contents
1. [dim_fund](#1-dim_fund)
2. [dim_date](#2-dim_date)
3. [fact_nav](#3-fact_nav)
4. [fact_transactions](#4-fact_transactions)
5. [fact_performance](#5-fact_performance)
6. [fact_aum](#6-fact_aum)
7. [sip_inflows](#7-sip_inflows)
8. [category_inflows](#8-category_inflows)
9. [folio_count](#9-folio_count)
10. [portfolio_holdings](#10-portfolio_holdings)
11. [benchmark_indices](#11-benchmark_indices)

---

## 1. dim_fund
**Source File:** `01_fund_master.csv`  
**Description:** Master dimension table containing profile information for each mutual fund scheme.  
**Rows:** 40  

| Column | Data Type | Description | Example |
|---|---|---|---|
| amfi_code | TEXT | Unique fund identifier assigned by AMFI (Association of Mutual Funds in India) | 119551 |
| fund_house | TEXT | Name of the Asset Management Company managing the fund | SBI Mutual Fund |
| scheme_name | TEXT | Full official name of the mutual fund scheme | SBI Bluechip Fund - Direct Plan |
| category | TEXT | Broad investment category of the fund | Equity, Debt, Hybrid |
| sub_category | TEXT | Specific sub-category under the broad category | Large Cap, Mid Cap |
| plan | TEXT | Type of plan — Direct or Regular | Direct, Regular |
| launch_date | TEXT | Date when the fund was launched | 01-01-2013 |
| benchmark | TEXT | Index used to measure fund performance | Nifty 50, BSE Sensex |
| expense_ratio_pct | REAL | Annual fee charged by fund as % of investment | 0.85 |
| exit_load_pct | REAL | Penalty fee charged on early withdrawal | 1.00 |
| min_sip_amount | REAL | Minimum monthly SIP investment allowed in ₹ | 500 |
| min_lumpsum_amount | REAL | Minimum one-time investment allowed in ₹ | 5000 |
| fund_manager | TEXT | Name of the person managing the fund | Rohit Singhania |
| risk_category | TEXT | SEBI defined risk level of the fund | Low, Moderate, High |
| sebi_category_code | TEXT | Official category code assigned by SEBI | EQ001 |

---

## 2. dim_date
**Source:** Built from `02_nav_history.csv` dates  
**Description:** Date dimension table breaking every date into parts for easy time-based filtering and analysis.  
**Rows:** 1,150  

| Column | Data Type | Description | Example |
|---|---|---|---|
| full_date | TEXT | Complete date in YYYY-MM-DD format | 2024-01-15 |
| day | INTEGER | Day of the month | 15 |
| month | INTEGER | Month number | 1 |
| year | INTEGER | Year | 2024 |
| quarter | INTEGER | Quarter of the year (1=Jan-Mar, 2=Apr-Jun, 3=Jul-Sep, 4=Oct-Dec) | 1 |
| day_of_week | TEXT | Name of the day | Monday |

---

## 3. fact_nav
**Source File:** `02_nav_history.csv`  
**Description:** Daily Net Asset Value (NAV) for each mutual fund scheme. NAV is the per-unit price of the fund.  
**Rows:** 46,000  

| Column | Data Type | Description | Example |
|---|---|---|---|
| amfi_code | TEXT | Fund identifier — links to dim_fund | 119551 |
| date | TEXT | Date of NAV in YYYY-MM-DD format | 2024-01-15 |
| nav | REAL | Net Asset Value (price per unit) in ₹ on that date | 45.23 |

---

## 4. fact_transactions
**Source File:** `08_investor_transactions.csv`  
**Description:** Every individual investor transaction — purchases and redemptions across all funds.  
**Rows:** 32,778  

| Column | Data Type | Description | Example |
|---|---|---|---|
| investor_id | TEXT | Unique identifier for each investor | INV003054 |
| transaction_date | TEXT | Date of transaction in YYYY-MM-DD format | 2024-01-15 |
| amfi_code | TEXT | Fund identifier — links to dim_fund | 119551 |
| transaction_type | TEXT | Type of transaction — only 3 allowed values | SIP, Lumpsum, Redemption |
| amount_inr | REAL | Transaction amount in Indian Rupees | 5000.00 |
| state | TEXT | Indian state where investor is located | Maharashtra |
| city | TEXT | City where investor is located | Mumbai |
| city_tier | TEXT | Classification of city by size | Tier 1, Tier 2, Tier 3 |
| age_group | TEXT | Age bracket of the investor | 25-35, 35-45 |
| gender | TEXT | Gender of the investor | Male, Female |
| annual_income_lakh | REAL | Investor's annual income in lakhs | 12.5 |
| payment_mode | TEXT | How the payment was made | Net Banking, UPI |
| kyc_status | TEXT | KYC verification status — only 2 allowed values | Verified, Pending |

---

## 5. fact_performance
**Source File:** `07_scheme_performance.csv`  
**Description:** Performance metrics, risk ratios, and ratings for each mutual fund scheme.  
**Rows:** 40  

| Column | Data Type | Description | Example |
|---|---|---|---|
| amfi_code | TEXT | Fund identifier — links to dim_fund | 119551 |
| scheme_name | TEXT | Name of the fund scheme | SBI Bluechip Fund |
| fund_house | TEXT | Name of the AMC | SBI Mutual Fund |
| category | TEXT | Fund category | Equity |
| plan | TEXT | Direct or Regular plan | Direct |
| return_1yr_pct | REAL | Fund return over last 1 year in % | 14.5 |
| return_3yr_pct | REAL | Fund return over last 3 years in % | 12.3 |
| return_5yr_pct | REAL | Fund return over last 5 years in % | 11.8 |
| benchmark_3yr_pct | REAL | Benchmark index return over 3 years in % | 11.2 |
| alpha | REAL | Excess return generated over benchmark | 1.1 |
| beta | REAL | Fund sensitivity to market movements (1=moves with market) | 0.95 |
| sharpe_ratio | REAL | Return earned per unit of risk taken | 1.2 |
| sortino_ratio | REAL | Return earned per unit of downside risk | 1.5 |
| std_dev_ann_pct | REAL | Annual volatility of the fund in % | 14.2 |
| max_drawdown_pct | REAL | Largest peak to trough fall in fund value in % | -18.5 |
| aum_crore | REAL | Total Assets Under Management in ₹ crore | 15234.5 |
| expense_ratio_pct | REAL | Annual fee charged as % of investment (Valid range: 0.1%–2.5%) | 0.85 |
| morningstar_rating | INTEGER | Morningstar star rating (1 to 5) | 4 |
| risk_grade | TEXT | Overall risk classification | Low, Moderate, High |

---

## 6. fact_aum
**Source File:** `03_aum_by_fund_house.csv`  
**Description:** Monthly Assets Under Management for each fund house. Tracks how much total money each AMC manages over time.  
**Rows:** 90  

| Column | Data Type | Description | Example |
|---|---|---|---|
| date | TEXT | Month end date | 2024-03-31 |
| fund_house | TEXT | Name of the Asset Management Company | SBI Mutual Fund |
| aum_lakh_crore | REAL | Total AUM in lakh crore ₹ | 6.05 |
| aum_crore | REAL | Total AUM in crore ₹ | 605000 |
| num_schemes | INTEGER | Number of schemes managed by fund house | 186 |

---

## 7. sip_inflows
**Source File:** `04_monthly_sip_inflows.csv`  
**Description:** Industry-wide monthly SIP inflow data showing growth trend of systematic investments.  
**Rows:** 48  

| Column | Data Type | Description | Example |
|---|---|---|---|
| month | TEXT | Month in YYYY-MM format | 2024-01 |
| sip_inflow_crore | REAL | Total SIP inflows in ₹ crore that month | 19000.5 |
| active_sip_accounts | REAL | Number of active SIP accounts | 8500000 |
| new_sip_registrations | REAL | New SIPs registered that month | 250000 |
| sip_aum_crore | REAL | Total AUM from SIP investments | 950000 |
| yoy_growth_pct | REAL | Year over year growth % (NULL for first year — no prior data to compare) | 15.3 |

---

## 8. category_inflows
**Source File:** `05_category_inflows.csv`  
**Description:** Monthly inflow data broken down by fund category showing which categories attract most investment.  
**Rows:** 144  

| Column | Data Type | Description | Example |
|---|---|---|---|
| month | TEXT | Month in YYYY-MM format | 2024-01 |
| category | TEXT | Fund category | Equity, Debt, Hybrid |
| inflow_crore | REAL | Total money flowing into that category in ₹ crore | 15000.5 |
| outflow_crore | REAL | Total money flowing out of that category in ₹ crore | 8000.2 |
| net_inflow_crore | REAL | Net inflow (inflow minus outflow) in ₹ crore | 7000.3 |

---

## 9. folio_count
**Source File:** `06_industry_folio_count.csv`  
**Description:** Monthly count of total investor folios (accounts) in the mutual fund industry.  
**Rows:** 21  

| Column | Data Type | Description | Example |
|---|---|---|---|
| month | TEXT | Month in YYYY-MM format | 2024-01 |
| total_folios | REAL | Total number of investor accounts industry wide | 16500000 |
| equity_folios | REAL | Folios in equity funds | 12000000 |
| debt_folios | REAL | Folios in debt funds | 2500000 |
| other_folios | REAL | Folios in other fund categories | 2000000 |

---

## 10. portfolio_holdings
**Source File:** `09_portfolio_holdings.csv`  
**Description:** Stock and bond holdings of each mutual fund — what each fund has invested in.  
**Rows:** 322  

| Column | Data Type | Description | Example |
|---|---|---|---|
| amfi_code | TEXT | Fund identifier — links to dim_fund | 119551 |
| stock_name | TEXT | Name of the stock or bond held | Reliance Industries |
| sector | TEXT | Business sector of the holding | Energy, Banking |
| holding_pct | REAL | Percentage of fund portfolio in this stock | 8.5 |
| market_value_crore | REAL | Market value of holding in ₹ crore | 1250.5 |

---

## 11. benchmark_indices
**Source File:** `10_benchmark_indices.csv`  
**Description:** Daily index values for benchmark indices used to compare fund performance.  
**Rows:** 8,050  

| Column | Data Type | Description | Example |
|---|---|---|---|
| date | TEXT | Date in YYYY-MM-DD format | 2024-01-15 |
| index_name | TEXT | Name of the benchmark index | Nifty 50, BSE Sensex |
| open | REAL | Opening index value that day | 21500.25 |
| high | REAL | Highest index value that day | 21750.80 |
| low | REAL | Lowest index value that day | 21450.10 |
| close | REAL | Closing index value that day | 21680.45 |

---

## Data Quality Notes
| Issue | Table | Status |
|---|---|---|
| Date format stored as DD-MM-YYYY in raw CSVs | fact_nav, fact_transactions | Fixed during loading — converted to YYYY-MM-DD |
| YOY growth NULL for 2022 rows | sip_inflows | Expected — no prior year data to compare |
| Schema design vs actual columns mismatch | All tables | Known issue — `if_exists=replace` overwrote schema design |
| No missing NAV values found | fact_nav | Data already clean |
| No duplicate transactions found | fact_transactions | Data already clean |