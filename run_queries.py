# run_queries.py
import sqlite3
import pandas as pd

conn = sqlite3.connect("bluestock_mf.db")
#replace the query inside """   """ with the particular query u want to run.
query = """
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
"""

df = pd.read_sql_query(query, conn)
print(df.to_string(index=False))
conn.close()