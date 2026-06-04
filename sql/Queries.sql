-- Query 1: Top 5 funds by AUM
-- Which funds managed most money?
SELECT
    scheme_name,
    fund_house,
    category,
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Query 2: average NAV per month
-- how has the average fund price changed month by month?
SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 2)      AS avg_nav_all_funds
FROM fact_nav
GROUP BY month
ORDER BY month ASC;

-- Query 3: SIP YoY growth
-- Is SIP investment growingg year over year?
SELECT
    month,
    sip_inflow_crore,
    active_sip_accounts_crore,
    yoy_growth_pct
FROM sip_inflows
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month ASC;

-- Query 4: Transaction by state
-- which state has highest mutual fund investment activity?
SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount_inr,
    ROUND(AVG(amount_inr),2) AS avg_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- Query 5: Funds with expense ratio < 1%
-- which funds offers the best value with lowest management fees?
SELECT
    scheme_name,
    fund_house,
    category,
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct ASC;

-- Query 6: total transaction amount by fund type
--  how much money came in via SIP, Lumpsum and Redemption?
SELECT
    transaction_type,
    COUNT(*) as total_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount_inr,
    ROUND(AVG(amount_inr),2) AS avg_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;

-- Query 7: KYC Status breakdown
-- How many investors are verified and how many are pending?
SELECT
    investor_id,
    kyc_status,
    COUNT(*) AS total_investors,
FROM fact_transactions
GROUP BY kyc_status;

-- Query 8: Fund beating their benchmark
-- How many funds gave better returns than benchmark?
SELECT
    scheme_name,
    fund_house,
    return_3yr_pct,
    benchmark_3yr_pct
FROM fact_transactions
WHERE return_3yr_pct > benchmark_3yr_pct;
-- OR --
SELECT  scheme_name, fund_house, return_3yr_pct, benchmark_3yr_pct,
    ROUND(return_3yr_pct-benchmark_3yr_pct,2) AS alpha_vs_benchmark,
    CASE
        WHEN return_3yr_pct > benchmark_3yr_pct THEN "Beat benchmark"
        ELSE "Below benchmark"
    END AS performance_vs_benchmark
FROM fact_performance
ORDER BY alpha_vs_benchmark DESC;

-- Query 9: Gender wise investment pattern
-- How do male vs female investors invest differently?
SELECT
    gender, transaction_type,
    COUNT(*) AS total_transactions,
    ROUND(AVG(amount_inr), 2)  AS avg_investment_amount
FROM fact_transactions
GROUP BY gender
ORDER BY total_transactions DESC;

-- Query 10: High risk vs low risk fund returns.
-- Do high risk funds actually give better returns?
SELECT
    risk_grade,
    COUNT(*) AS num_funds,
    ROUND(AVG(return_1yr_pct),2) AS avg_1yr_return,
    ROUND(AVG(return_3yr_pct),2) AS avg_3yr_return,
    ROUND(AVG(return_5yr_pct),2) AS avg_5yr_return,
    ROUND(AVG(expense_ratio_pct),2) AS avg_expense_ratio
FROM fact_performance
GROUP BY risk_grade
ORDER BY avg_1yr_return DESC;



























    