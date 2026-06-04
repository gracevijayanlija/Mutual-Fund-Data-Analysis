-- schema.sql
-- Star Schema for Mutual Fund Analytics
-- Day 2: SQLite Database Design

-- ══════════════════════════════════════════
-- DIMENSION TABLE 1: dim_fund
-- Stores master info about each fund
-- ══════════════════════════════════════════
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    -- AUTOINCREMENT means SQLite automatically assigns 1, 2, 3...
    amfi_code     TEXT NOT NULL UNIQUE,
    -- UNIQUE means no two funds can have same amfi_code
    scheme_name   TEXT NOT NULL,
    fund_house    TEXT,
    category      TEXT,
    plan          TEXT
);

-- ══════════════════════════════════════════
-- DIMENSION TABLE 2: dim_date
-- Breaks every date into parts for easy filtering
-- ══════════════════════════════════════════
CREATE TABLE IF NOT EXISTS dim_date (
    date_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date     TEXT NOT NULL UNIQUE,
    -- Stored as text: "2024-01-15"
    day           INTEGER,
    month         INTEGER,
    year          INTEGER,
    quarter       INTEGER,
    -- 1=Jan-Mar, 2=Apr-Jun, 3=Jul-Sep, 4=Oct-Dec
    day_of_week   TEXT
    -- "Monday", "Tuesday" etc
);

-- ══════════════════════════════════════════
-- FACT TABLE 1: fact_nav
-- Daily NAV values for each fund
-- ══════════════════════════════════════════
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id       INTEGER NOT NULL,
    date_id       INTEGER NOT NULL,
    nav           REAL NOT NULL,
    -- REAL means decimal number like 45.23
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
    -- These two lines connect fact_nav to dim_fund and dim_date
);

-- ══════════════════════════════════════════
-- FACT TABLE 2: fact_transactions
-- Every investor transaction
-- ══════════════════════════════════════════
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id       TEXT NOT NULL,
    fund_id           INTEGER NOT NULL,
    date_id           INTEGER NOT NULL,
    transaction_type  TEXT CHECK(transaction_type IN ('SIP','Lumpsum','Redemption')),
    -- CHECK means only these 3 values are allowed
    amount            REAL NOT NULL,
    units             REAL,
    nav_at_transaction REAL,
    kyc_status        TEXT CHECK(kyc_status IN ('Verified','Pending')),
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- ══════════════════════════════════════════
-- FACT TABLE 3: fact_performance
-- Fund returns and risk metrics
-- ══════════════════════════════════════════
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id           INTEGER NOT NULL,
    return_1yr_pct    REAL,
    return_3yr_pct    REAL,
    return_5yr_pct    REAL,
    benchmark_3yr_pct REAL,
    alpha             REAL,
    beta              REAL,
    sharpe_ratio      REAL,
    sortino_ratio     REAL,
    std_dev_ann_pct   REAL,
    max_drawdown_pct  REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade        TEXT,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id)
);

-- ══════════════════════════════════════════
-- FACT TABLE 4: fact_aum
-- Monthly AUM per fund house
-- ══════════════════════════════════════════
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id       INTEGER,
    date_id       INTEGER NOT NULL,
    fund_house    TEXT,
    aum_crore     REAL NOT NULL,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);